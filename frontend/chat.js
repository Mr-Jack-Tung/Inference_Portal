import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import { FormControl, FormLabel } from '@mui/material';
import Grid from '@mui/material/Grid';
import { styled } from '@mui/material/styles';
import InputLabel from '@mui/material/InputLabel';
import Checkbox from '@mui/material/Checkbox';
import Radio from '@mui/material/Radio';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import RadioGroup from '@mui/material/RadioGroup';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import FormControlLabel from '@mui/material/FormControlLabel';
import Slider from '@mui/material/Slider';
import Container from '@mui/material/Container';
import InputAdornment from '@mui/material/InputAdornment';
import Switch from '@mui/material/Switch';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import { useSearchParams } from 'react-router-dom';
import List from '@mui/material/List';
import ListItemText from '@mui/material/ListItemText';
import TextField from '@mui/material/TextField';
import Divider from '@mui/material/Divider';
import Link from '@mui/material/Link';
import ApiIcon from '@mui/icons-material/Api';
import ArticleIcon from '@mui/icons-material/Article';
import PrecisionManufacturingIcon from '@mui/icons-material/PrecisionManufacturing';
import LayersIcon from '@mui/icons-material/Layers';
import ChatIcon from '@mui/icons-material/Chat';
import KeyIcon from '@mui/icons-material/Key';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import EmailIcon from '@mui/icons-material/Email';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { useMatch } from "react-router-dom";
import SearchIcon from '@mui/icons-material/Search';
import DirectionsIcon from '@mui/icons-material/Directions';
import SendIcon from '@mui/icons-material/Send';
const ChatPaper = styled(Paper)(({ theme }) => ({
    minWidth: 660,
    height: 700,
    padding: theme.spacing(2),
    ...theme.typography.body2,
}));
const ChatInput = styled(TextField)(({ theme }) => ({
    width: '100%',
    ...theme.typography.body2,
}));

function Chat() {
    const [model_objects, setModels] = useState([]);
    const [chat_message, setChatMessage] = useState([]);
    const [agent_objects, setAgents] = useState([]);
    const [choosen_model, setChoosenModel] = useState("gpt-4");
    const [top_p, setTopp] = useState(0.72);
    const [top_k, setTopk] = useState(-1);
    const [mode, setMode] = useState("chat");
    const [max_tokens, setMaxToken] = useState(512);
    const [usememory, setUseMemory] = useState(true);
    const [temperature, setTemperature] = useState(0.73);
    const [beam, setBeam] = useState(false);
    const [earlystopping, setEarlyStopping] = useState(false);
    const [presencepenalty, setPresencePenalty] = useState(0);
    const [frequencypenalty, setFrequencyPenalty] = useState(0);
    const [lengthpenalty, setLengthPenalty] = useState(0);
    const handleChange = (event) => {
     
        if (switch_name == "beam") {
            setBeam(!event)
         
        }
      };
    useEffect(() => {
        axios.all([
            axios.get('/frontend-api/model'),
        ])
            .then(axios.spread((model_object) => {
                setModels(model_object.data.models);
                setAgents(model_object.data.models_agent);
            }))
            .catch(error => {
                console.log(error);
            });
    }, []);

    const submitChat = () => {
        console.log({
            "top_p": top_p,
            "top_k": top_k,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "choosen_models": choosen_model,
            "lengthpenalty": lengthpenalty,
            "frequencypenalty": frequencypenalty,
            "presencepenalty": presencepenalty,
            "beam": beam,
            "use_memory": usememory,
            "mode": mode,
            "early_stopping": earlystopping
        })
    }
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    const [searchParams] = useSearchParams();

    const type = searchParams.get("type");
    var url = window.location.pathname.split("/").filter(path => path !== "")
    useEffect(() => {
    const websocket = new W3CWebSocket(ws_scheme + '://127.0.0.1:8000/ws/' + url[url.length - 2] +'/' + url[url.length - 1] + '/');
    websocket.onopen = () => {
        console.log("WebSocket Client Connected");
      };
    websocket.onmessage = (message) => {
        const dataFromServer = JSON.parse(message.data);
        if (dataFromServer) {
            setChatMessage([
                ...chat_message,
                dataFromServer,
            ])
         console.log(dataFromServer)
          };
        }
    }, []);
    return (
        <Container maxWidth="lg" sx={{ width: 1200 }}>
            <title>Chat</title>
            <Box m={2}>
                <Grid container spacing={2}>
                    <Grid item md={8}>
                        <ChatPaper variant="outlined">
                        {chat_message.map((mess) => {
                                        return (
                                            <div key={mess.time}>{mess.message} ({mess.role} {mess.time})</div> 
                                        )
                                    })}

                        </ChatPaper>
                        <Box mt={2}>
                            <Paper
                                component="form"
                                sx={{ p: '2px 4px', display: 'flex', minWidth: 660 }}
                            >
                                <ChatInput
                                    id="standard-multiline-flexible"
                                    multiline
                                    maxRows={6}
                                    minRows={4}
                                    variant="standard"
                                    InputProps={{
                                        endAdornment: <InputAdornment sx={{ position: 'absolute', bottom: 30, right: 10 }} position="end"> 
                                        <  Button sx={{ height: 32, }} variant="contained" size="small" onClick={submitChat} endIcon={<SendIcon />}>Send</Button></InputAdornment>,
                                    }}
                                />

                            </Paper>

                        </Box>
                    </Grid>
                    <Grid item md={4}>
                        <FormControl defaultValue="">
                            <Stack direction='column' spacing={1}>
                                <InputLabel id="demo-simple-select-label">Models</InputLabel>
                                <Select
                                    labelId="demo-simple-select-label"
                                    id="demo-simple-select"
                                    onChange={e => setChoosenModel(e.target.value)}
                                    value={choosen_model}
                                    label="Models"
                                >
                                    {model_objects.map((model_object_) => {
                                        return (
                                            <MenuItem key={model_object_.name} value={model_object_.name}>{model_object_.name}</MenuItem>
                                        )
                                    })}
                                    {agent_objects.map((agent_object_) => {
                                        return (
                                            <MenuItem key={agent_object_.name} value={agent_object_.name}>{agent_object_.name}</MenuItem>
                                        )
                                    })}
                                </Select>
                                <Divider></Divider>
                                <FormLabel id="demo-radio-buttons-group-label">Parameters</FormLabel>
                                <FormControlLabel control={<Switch defaultChecked onChange={e => setUseMemory(e.target.checked)} />} label="Use Memory" />
                                <RadioGroup
                                    defaultValue="chat"
                                    name="radio-buttons-group"
                                    onChange={e => setMode(e.target.value)}
                                    value={mode}
                                >
                                    <FormControlLabel key="chat" value='chat' control={<Radio size="small" />} label="Chat Bot Mode" />
                                    <FormControlLabel key="generate" value='generate' control={<Radio size="small" />} label="Sentence Completion" />
                                    <Divider></Divider>

                                </RadioGroup>
                                <Typography gutterBottom>Top_p: {top_p}</Typography>
                                <Slider
                                    step={0.01}
                                    min={0}
                                    max={1}
                                    valueLabelDisplay="off"
                                    onChange={e => setTopp(e.target.value)}
                                    value={top_p}
                                />
                                <Typography gutterBottom>Top_k: {top_k}</Typography>
                                <Slider
                                    defaultValue={-1}
                                    step={1}
                                    min={-1}
                                    max={100}
                                    valueLabelDisplay="off"
                                    onChange={e => setTopk(e.target.value)}
                                    value={top_k}
                                />
                                <Typography gutterBottom>Max_tokens: {max_tokens}</Typography>
                                <Slider
                                    defaultValue={512}
                                    step={1}
                                    min={1}
                                    max={4090}
                                    onChange={e => setMaxToken(e.target.value)}
                                    value={max_tokens}
                                    valueLabelDisplay="off"
                                />
                                <Typography gutterBottom>Temperature: {temperature}</Typography>
                                <Slider
                                    defaultValue={0.73}
                                    step={0.01}
                                    min={0}
                                    max={1}
                                    onChange={e => setTemperature(e.target.value)}
                                    value={temperature}
                                    valueLabelDisplay="off"
                                />
                                <Typography gutterBottom>Presence penalty: {presencepenalty}</Typography>
                                <Slider
                                    aria-label="Small steps"
                                    defaultValue={0}
                                    step={0.01}
                                    min={-2}
                                    max={2}
                                    onChange={e => setPresencePenalty(e.target.value)}
                                    value={presencepenalty}
                                    valueLabelDisplay="off"
                                />
                                <Typography gutterBottom>Frequency penalty: {frequencypenalty}</Typography>
                                <Slider
                                    aria-label="Small steps"
                                    defaultValue={0}
                                    step={0.01}
                                    min={-2}
                                    max={2}
                                    onChange={e => setFrequencyPenalty(e.target.value)}
                                    value={frequencypenalty}
                                    valueLabelDisplay="off"
                                />
                                <Divider></Divider>
                                <FormControlLabel control={<Switch
                                    onChange={e => setBeam(e.target.checked)}
                                    value={beam}
                                />} label="Beam Search: " />
                                <FormControlLabel control={<Switch
                                    onChange={e => setEarlyStopping(e.target.checked)}
                                    value={earlystopping}
                                />} label="Early Stopping: " />
                                <Typography gutterBottom>Length penalty: {lengthpenalty}</Typography>
                                <Slider
                                    onChange={e => setLengthPenalty(e.target.value)}
                                    value={lengthpenalty}
                                    defaultValue={2}
                                    step={1}
                                    min={1}
                                    max={5}
                                    valueLabelDisplay="off"
                                />
                            </Stack>
                        </FormControl>

                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
}

export default Chat;
