import json
import uuid
from datetime import datetime
from django.core.cache import cache
from apikey.models import APIKEY, InstructionTree
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from apikey.celery_tasks import Agent_Inference

from apikey.util import constant
from apikey.pydantic_validator import (
                                 AgentSchemaInstruct,
                                 AgentSchemaMessage,
                                 AgentSchemaParagraph,
                                 AgentSchemaTemplate,
                                 )
import regex as re
from pydantic import ValidationError



class Consumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def check_key(self):
        try:
            key = APIKEY.objects.get_from_key(self.key)
            return key
        except APIKEY.DoesNotExist:
            return False

    async def get_template(self, name):
        try:
            template = await InstructionTree.objects.aget(name=name)
            return template
        except InstructionTree.DoesNotExist:
            return False
        
    @database_sync_to_async
    def get_child_tempalte_name(self, template, name=None):
        try:
            if name is None:
                child_template = InstructionTree.objects.get(
                    name=template).get_leafnodes()
                return {"name_list": [c.name for c in child_template], "default_child": child_template[0].name, "default_instruct": child_template[0].instruct}
            else:
                child_template = InstructionTree.objects.get(name=name)
                return child_template.instruct
        except Exception as e:
            return e

    async def connect(self):
        self.url = self.scope["url_route"]["kwargs"]["key"]
        self.time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        self.max_turns = constant.DEFAULT_AGENT_TURN
        self.current_turn = 0
        self.session_history = []
        self.working_paragraph = str()
        self.is_session_start_node = True
        self.model_type = ""
        self.room_group_name = "agent_%s" % self.url
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Default to GPT4 or choose model on the left", "role": "Server", "time": self.time}))
        await self.send(text_data=json.dumps({"message": "Instruction to the user:\n\
                                              1. Click on the paragraph that you want to work on, then give the agent instructions to write \n\
                                              2. If you face any bug, refresh and retry.\n\
                                              3. Shift-Enter to drop line in chatbox.\n\
                                              4. You can export all paragraphs by clicking on [Export] on the right.",
                                              "role": "Server", "time": self.time}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'paragraph' in text_data_json:
            try:
                paragraph = AgentSchemaParagraph.model_validate_json(
                    text_data).paragraph
                if self.working_paragraph != paragraph:
                    self.working_paragraph = paragraph
                    self.current_turn = 0
                    self.session_history = []
                    await self.send(text_data=json.dumps({"message": f"Working on block {paragraph}, what do you want me to write?", "role": "Server", "time": self.time}))
                    await self.send(text_data=json.dumps({"paragraph": paragraph}))

            except ValidationError as e:
                await self.send(text_data=json.dumps({"message": f"Error: {e.errors()}", "role": "Server", "time": self.time}))
        elif 'swap_template' in text_data_json:
            try:
                swap = AgentSchemaTemplate.model_validate_json(
                    text_data).swap_template
                swap_template = await self.get_template(swap)
                child_template = await self.get_child_tempalte_name(swap_template, None)
                swap_instruction = swap_template.instruct
                swap_template_ = swap_template.default_editor_template
                await self.send(text_data=json.dumps({"message": f"Swap to {text_data_json['swap_template']}, what do you want me to write?", "role": "Server", "time": self.time}))
                await self.send(text_data=json.dumps({"swap_instruction": swap_instruction,
                                                      "swap_template": swap_template_,
                                                      "child_template_name_list": child_template['name_list'],
                                                      "default_child": child_template['default_child'],
                                                      "default_child_instruct": child_template['default_instruct']}))
            except ValidationError as e:
                await self.send(text_data=json.dumps({"message": f"Error: {e.errors()}", "role": "Server", "time": self.time}))
        elif 'swap_child_instruct' in text_data_json:
            try:
                swap_child_instruct = AgentSchemaInstruct.model_validate_json(
                    text_data).swap_child_instruct
                child_instruct = await self.get_child_tempalte_name(None, swap_child_instruct)
                await self.send(text_data=json.dumps({"child_instruct": child_instruct}))
            except ValidationError as e:
                await self.send(text_data=json.dumps({"message": f"Error: {e.errors()}", "role": "Server", "time": self.time}))
        elif 'message' in text_data_json:
            try:
                validated = AgentSchemaMessage.model_validate_json(text_data)
                self.key = validated.key
                key_object = cache.get(f"{self.key}")
                if key_object is None:
                    key_object = await self.check_key()
                if not key_object:
                    await self.send(text_data=json.dumps({"message": "Your key or key name is wrong, disconnected! Refresh the page to try again", "role": "Server", "time": self.time}))
                    await self.disconnect(self)
                elif not text_data_json["message"].strip():
                    await self.send(text_data=json.dumps({"message": "Empty string recieved", "role": "Server", "time": self.time}))
                elif key_object and text_data_json["message"].strip():
                    cache.set(f"{self.key}", key_object,
                              constant.CACHE_AUTHENTICATION)
                    agent_instruction = validated.agent_instruction
                    child_instruction = validated.child_instruction
                    current_turn_inner = self.current_turn
                    currentParagraph = validated.currentParagraph
                    self.working_paragraph = currentParagraph
                    message = validated.message
                    self.model_type = validated.choosen_models
                    choosen_template = validated.choosen_template
                    role = validated.role
                    unique_response_id = str(uuid.uuid4())
                    top_p = validated.top_p
                    max_tokens = validated.max_tokens
                    frequency_penalty = validated.frequency_penalty
                    presence_penalty = validated.presence_penalty
                    temperature = validated.temperature
                    agent_instruction += child_instruction
                    Agent_Inference.delay(
                        is_session_start_node=self.is_session_start_node, 
                        unique=unique_response_id,
                        key=self.key,
                        stream=True,
                        message=message,
                        credit=key_object.credit,
                        room_group_name=self.room_group_name,
                        model=choosen_template,
                        max_turns=self.max_turns,
                        current_turn_inner=current_turn_inner,
                        agent_instruction=agent_instruction,
                        session_history=self.session_history,
                        model_type=self.model_type,
                        frequency_penalty=frequency_penalty,
                        top_p=top_p,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        presence_penalty=presence_penalty,
                    )

                    await self.channel_layer.group_send(
                        self.room_group_name, {"type": "chat_message",
                                               "role": role,
                                               "message": message,
                                               "credit": key_object.credit,
                                               "unique": unique_response_id,
                                               "choosen_model":  choosen_template,
                                               "current_turn": current_turn_inner
                                               }
                    )
            except ValidationError as e:
                await self.send(text_data=json.dumps({"message": f"Error: {e.errors()}", "role": "Server", "time": self.time}))

    async def chat_message(self, event):
        if "max_turn_reached" in event:
            await self.send(text_data=json.dumps({"message": f"Max Turns reached, click on the paragraphs on the left to write again", "role": "Server", "time": self.time}))
        if "session_history" in event:
            self.session_history = event['session_history']
            self.current_turn = event['current_turn']
        if "message" in event:
            message = event["message"]
            role = event["role"]
            credit = event["credit"]
            self.time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # Send message to WebSocket
            if role == "Human" or role == "Server":
                await self.send(text_data=json.dumps({"message": message, "role": role,  "time": self.time}))
                if role == "Human":
                    self.is_session_start_node = False
                    unique_response_id = event['unique']
                    await self.send(text_data=json.dumps({"holder": "place_holder",  "holderid":  unique_response_id, "role": event['choosen_model'], "time": self.time, "credit": credit}))
            else:
                unique_response_id = event['unique']
                await self.send(text_data=json.dumps({"message": message,  "stream_id":  unique_response_id, "credit": credit}))

        if "agent_action" in event:
            agent_action = event['agent_action']
            if agent_action == "STOP":
                full_result = self.session_history[-1]['content']
                full_result = full_result.replace('{"Action": "STOP"}', "")
                full_result = full_result.replace("Final Answer:", "")
                thought_match = re.findall("Thought: (.*)\n", full_result)
                full_result = full_result.replace(thought_match[0], "")
                full_result = full_result.replace("Thought:", "")
                full_result = full_result.replace("\n\n\n", "")
                await self.send(text_data=json.dumps({"message": f"Your request is finished, the result is moved to the textbox on the left", "role": "Server", "time": self.time}))
                await self.send(text_data=json.dumps({"agent_action": agent_action, "result_id": self.working_paragraph, "full_result": full_result}))
                self.session_history = []
                self.current_turn = 0