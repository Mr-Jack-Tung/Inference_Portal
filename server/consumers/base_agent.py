import json

import pytz
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from pydantic import ValidationError

from server.consumers.pydantic_validator import (
    AgentSchemaInstruct,
    AgentSchemaParagraph,
    AgentSchemaTemplate,
)
from server.models.log import PromptResponse
from server.rate_limit import RateLimitError, rate_limit_initializer
from server.utils.async_.async_inference import (
    AsyncInferenceOpenaiMixin,
    AsyncInferenceVllmMixin,
)
from server.utils.async_.async_query_database import QueryDBMixin


class BaseAgent(
    AsyncWebsocketConsumer,
    AsyncInferenceOpenaiMixin,
    AsyncInferenceVllmMixin,
    QueryDBMixin,
):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.current_turn = 0
        self.session_history = []
        self.is_session_start_node = None
        self.working_paragraph = None
        self.use_summary = False
        self.permission_code = "server.allow_agent"
        self.destination = "Agents"
        self.type = PromptResponse.PromptType.AGENT

    async def connect(self):
        self.url = self.scope["url_route"]["kwargs"]["key"]
        self.timezone = self.scope["url_route"]["kwargs"]["tz"]
        self.time = timezone.localtime(
            timezone.now(), pytz.timezone(self.timezone)
        ).strftime("%Y-%m-%d %H:%M:%S")
        self.user = self.scope["user"]
        self.key_object, self.master_user, self.slave_key_object = (
            await self.get_master_key_and_master_user()
        )
        self.rate_limiter = await rate_limit_initializer(
            key_object=self.key_object,
            strategy="moving_windown",
            slave_key_object=self.slave_key_object,
            namespace=self.type.label,
            timezone=self.timezone,
        )
        self.room_group_name = f"{self.destination}{self.url}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        is_authorised = await self.check_permission(
            permission_code=self.permission_code, destination=self.destination
        )

        if is_authorised and self.backend:
            await self.send_connect_message()
            await self.send(
                text_data=json.dumps(
                    {
                        "message": """Instruction to the user:\n1. Click on the paragraph that you want to work on, then give the agent instructions to write \n2. If you face any bug, refresh and retry.\n3. Shift-Enter to drop line in chatbox.\n4. You can export all paragraphs by clicking on [Export] on the left.""",
                        "role": "Server",
                        "time": self.time,
                    }
                )
            )

    async def send_connect_message(self):
        await self.send(
            text_data=json.dumps(
                {
                    "message": f"You are currently using {self.backend} backend. Default to GPT4 or choose model on the right.",
                    "role": "Server",
                    "time": self.time,
                }
            )
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):
        try:
            await self.rate_limiter.check_rate_limit()
            await self.send_message_if_not_rate_limited(text_data)
            text_data_json = json.loads(text_data)
            if "paragraph" in text_data_json:
                try:
                    paragraph = AgentSchemaParagraph.model_validate_json(
                        text_data
                    ).paragraph
                    if self.working_paragraph != paragraph:
                        self.working_paragraph = paragraph
                        if not self.use_summary:
                            self.current_turn = 0
                            self.session_history = []
                            await self.send(
                                text_data=json.dumps(
                                    {
                                        "message": f"Working on block {paragraph}, what do you want me to write?",
                                        "role": "Server",
                                        "time": self.time,
                                    }
                                )
                            )
                        else:
                            await self.send(
                                text_data=json.dumps(
                                    {
                                        "message": f"Working on block {paragraph}",
                                        "role": "Server",
                                        "time": self.time,
                                    }
                                )
                            )
                        await self.send(text_data=json.dumps({"paragraph": paragraph}))

                except ValidationError as e:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "message": f"Error: {e.errors()}",
                                "role": "Server",
                                "time": self.time,
                            }
                        )
                    )
            elif "swap_template" in text_data_json:
                try:
                    data = AgentSchemaTemplate.model_validate_json(text_data)
                    swap = data.swap_template
                    template_type = data.template_type
                    swap_template = await self.get_template(swap, template_type)
                    child_template = await self.get_child_template_list(
                        swap_template, template_type
                    )
                    swap_instruction = swap_template.instruct
                    swap_template_ = swap_template.default_editor_template
                    self.current_turn = 0
                    self.session_history = []

                    await self.send(
                        text_data=json.dumps(
                            {
                                "message": f"Swap to {swap_template.name if template_type == 'system' else swap_template.displayed_name}, what do you want me to write?",
                                "role": "Server",
                                "time": self.time,
                            }
                        )
                    )
                    await self.send(
                        text_data=json.dumps(
                            {
                                "swap_instruction": swap_instruction,
                                "swap_template": swap_template_,
                                "child_template_name_list": child_template["name_list"],
                                "child_template_displayed_name_list": (
                                    []
                                    if template_type == "system"
                                    else child_template["displayed_name_list"]
                                ),
                                "default_child": child_template["default_child"],
                                "default_child_instruct": child_template[
                                    "default_instruct"
                                ],
                            }
                        )
                    )
                except ValidationError as e:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "message": f"Error: {e.errors()}",
                                "role": "Server",
                                "time": self.time,
                            }
                        )
                    )
            elif "swap_child_instruct" in text_data_json:
                try:
                    data = AgentSchemaInstruct.model_validate_json(text_data)
                    swap_child_instruct = data.swap_child_instruct
                    template_type = data.template_type
                    child_instruct = await self.get_template(
                        swap_child_instruct, template_type
                    )
                    child_instruct = child_instruct.instruct
                    self.current_turn = 0
                    self.session_history = []
                    await self.send(
                        text_data=json.dumps({"child_instruct": child_instruct})
                    )
                except ValidationError as e:
                    await self.send(
                        text_data=json.dumps(
                            {
                                "message": f"Error: {e.errors()}",
                                "role": "Server",
                                "time": self.time,
                            }
                        )
                    )

        except RateLimitError as e:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": e.message,
                        "role": "Server",
                        "time": self.time,
                    }
                )
            )

    async def send_message_if_not_rate_limited(self):
        raise NotImplementedError("Implemented in child class!")
