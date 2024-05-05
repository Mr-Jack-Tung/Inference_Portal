import $ from 'jquery'
import React, { useEffect, useRef, useState } from "react"
import axios from 'axios';
import Container from '@mui/material/Container';
import ResponsiveAppBar from './component/navbar';
import DataTable from 'datatables.net-dt';
import jszip from 'jszip';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import pdfmake from 'pdfmake';
import Box from '@mui/material/Box';
import 'datatables.net-buttons-dt';
import 'datatables.net-buttons/js/buttons.colVis.mjs';
import Paper from '@mui/material/Paper';
import 'datatables.net-buttons/js/buttons.html5.mjs';
import 'datatables.net-buttons/js/buttons.print.mjs';
require('./component/dataTables.dataTables.css')
function Log() {
    $.DataTable = require('datatables.net')
    const tableRef = useRef()
    useEffect(() => {
        var url = window.location.pathname.split("/").filter(path => path !== "")
        $.fn.dataTable.ext.errMode = () => alert('You need to login before viewing log!');
        const table = $(tableRef.current).DataTable(
            {
                layout: {
                    topStart: 'pageLength',
                    top2Start: {
                        buttons: ['copyHtml5', 'excelHtml5', 'csvHtml5', 'pdfHtml5', 'print',],
                    }
                },
                columns: [
                    { title: "No." },
                    { title: "Prompts" },
                    { title: "Response" },
                    { title: "Models" },
                    { title: "Created Time" },
                    { title: "Type" },
                    { title: "Input Cost" },
                    { title: "Onput Cost" },
                    { title: "Input Tokens" },
                    { title: "Onput Tokens" }
                ],
                processing: true,
                serverSide: true,
                ajax: "/log/" + url[url.length - 1],
                responsive: true,
                destroy: true,
            }
        )

        return function () {
            table.destroy()
        }

    }, [])

    return (
        <Container maxWidth={false} disableGutters>
            <title>Models</title>
            <ResponsiveAppBar />
            <Container maxWidth="xl">
                <Box m={5} sx={{ overflow: 'auto' }}>
                    <Paper sx={{ overflow: 'auto' }} p={5}>
                        <table className="display" width="100%" ref={tableRef}></table>
                    </Paper>
                </Box>
            </Container >
        </Container>
    );
}

export default Log;