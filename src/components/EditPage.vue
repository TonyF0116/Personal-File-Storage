<template>
    <div class="page_title">{{ page_title }}</div>
    <div v-if="file_type == 0">
        <img :src="`/api/edit/get_file?file_id=${this.file_id}&account_id=${this.account_id}`" class="image" alt="image">
    </div>
    <div v-if="file_type == 1">
        <h3>Total page: {{ total_page_num }}, Cur page: {{ cur_page }}</h3>
        <div class="prev_next_button">
            <button @click="prev_page">Prev</button>
            <button @click="next_page">Next</button>
        </div>
        <canvas ref="canvas"></canvas>
    </div>
    <div v-if="file_type == 2">
        <table>
            <tbody>
                <tr v-for="(row, row_index) in excel_data" :key="row_index">
                    <td v-for="(cell, cell_index) in row" :key="cell_index">
                        <input v-model="excel_data[row_index][cell_index]">
                    </td>
                    <button style="margin-top: 18px;margin-left: -100px;" @click="add_cell(row)">Add Cell</button>
                </tr>
                <button style="margin-top: 10px;" @click="add_row">Add Row</button>
            </tbody>
        </table>
        <button @click="save_excel">Save</button>
    </div>
</template>

<script>

import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';

import { GlobalWorkerOptions, getDocument } from 'pdfjs-dist/build/pdf';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';
GlobalWorkerOptions.workerSrc = pdfjsWorker;

import { read, utils } from 'xlsx';

export default {
    data() {
        return {
            page_title: 'Edit Page',
            file_id: null,
            account_id: null,
            file_type: null,
            total_page_num: null,
            cur_page: 1,
            excel_data: [],
        }
    },
    mounted() {
        axios.defaults.headers.common['Authorization'] = this.$route.query.Authorization;
        this.initialize_edit_page();

    },
    methods: {
        // Send the server the updated excel file data
        save_excel() {
            axios.post('/api/edit/save_excel?file_id=' + this.file_id, this.excel_data)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
        },

        // Add row or cell
        add_row() {
            this.excel_data.push(['']);
        },
        add_cell(row) {
            row.push('');
        },

        // Load excel file function
        load_excel() {
            axios.get('/api/edit/get_file?file_id=' + this.file_id + '&account_id=' + this.account_id, { responseType: 'arraybuffer' })
                // axios.get('http://127.0.0.1:5000/api/edit/get_file?file_id=5&account_id=1', { responseType: 'arraybuffer' })
                .then((response) => {
                    const data = new Uint8Array(response.data);
                    const workbook = read(data, { type: 'array' });
                    this.excel_data = utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1 });
                })
                .catch((error) => {
                    console.error(error);
                });
        },



        prev_page() {
            if (this.cur_page == 1) {
                this.cur_page = this.total_page_num;
            } else {
                this.cur_page = this.cur_page - 1;
            }
            this.load_pdf();
        },
        next_page() {
            if (this.cur_page == this.total_page_num) {
                this.cur_page = 1;
            } else {
                this.cur_page = this.cur_page + 1;
            }
            this.load_pdf();
        },
        async load_pdf() {
            // Load file
            const url = '/api/edit/get_file?file_id=' + this.file_id + '&account_id=' + this.account_id;
            const loadingTask = getDocument(url);

            try {
                const pdf = await loadingTask.promise;
                this.total_page_num = pdf.numPages;

                const page = await pdf.getPage(this.cur_page);
                const canvas = this.$refs.canvas;

                const viewport = page.getViewport({ scale: 1.5 });
                canvas.width = viewport.width;
                canvas.height = viewport.height;

                const renderContext = {
                    canvasContext: canvas.getContext('2d'),
                    viewport,
                };
                await page.render(renderContext);
            } catch (error) {
                console.error('Error loading PDF:', error);
            }
        },
        // Authorization Validation
        initialize_edit_page() {
            this.file_id = this.$route.query.file_id;
            axios.post('/api/edit?file_id=' + this.file_id, {}
            ).then(response => {
                this.account_id = response.data.data.account_id;
                this.file_type = response.data.data.file_type;
                console.log(response);
                if (this.file_type == 1) {
                    this.load_pdf();
                } else if (this.file_type == 2) {
                    this.load_excel();
                }

            }, error => {
                console.log(error);
                if (error.response.status == 302 || error.response.status == 401) {
                    this.$router.push(error.response.data.data.redirection);
                }
            })
        },
    }
}

</script>

<style>
.prev_next_button {
    position: absolute;
    margin-top: -40px;
    right: 20%;
}

.page_title {
    font-family: Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    font-size: xxx-large;
}

.image {
    margin-top: 120px;
    max-width: 1000px;
    max-height: 1000px;
}
</style>