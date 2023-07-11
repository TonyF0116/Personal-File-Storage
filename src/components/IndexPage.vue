<template>
    <img :src="`/avatar?account_id=${this.account_id}&suffix=${this.avatar_suffix}`" class="avatar" alt="avatar">
    <h3 style="text-align: right;">Welcome, {{ name }}</h3>
    <div class="page_title">{{ page_title }}</div>

    <button class="generate_button" @click="generate_file_stat">Generate File Stat</button>

    <button class="upload_button" @click="show_popup">Upload</button>
    <transition name="fade">
        <div v-if="is_pop_up_visible" class="popup" @click.self="close_popup">
            <div class="popup_content">
                <input type="file" id="fileInput" @change="choose_file_clicked"
                    accept=".jpg, .jpeg, .png, .pdf, .xls, .xlsx">
                <label for="fileInput" class="choose_file_button">Choose File</label>

                <p>{{ choose_file_message }}</p>
                <div v-if="choose_file_message != '' && choose_file_message != 'Unaccepted file format'">
                    <button class="submit_button" @click="upload_file">Submit</button>
                    <p>{{ upload_msg }}</p>
                </div>


            </div>
        </div>
    </transition>

    <ol>
        <li v-for="file in  files " :key="file"><a
                :href="'/edit?file_id=' + file[0] + '&Authorization=' + this.$route.query.Authorization"
                style="float: left;">
                {{ file[2] }}
            </a>
            <span style="text-align: center;"> {{ file[4] }} </span>

            <span style="right: 0%;"><a :href="'/api/index/download?file_id=' + file[0] + '&Authorization='
                + this.$route.query.Authorization" :download=file[2]> Download</a>
            </span>
            <button @click="delete_file(file[0])" style="right: 0%;">Delete</button>

            <hr>
        </li>
    </ol>
</template>

<script>
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000';


export default {
    data() {
        return {
            page_title: 'Index Page',
            account_id: 0,
            name: "",
            administration: 0,
            avatar_suffix: "suffix",
            files: null,

            is_pop_up_visible: false,
            choose_file_message: "",
            upload_msg: "",
            file_to_upload: null,
        }
    },
    mounted() {
        axios.defaults.headers.common['Authorization'] = this.$route.query.Authorization;
        this.initialize_index_page();
    },
    methods: {
        // Delete file
        delete_file(file_id) {
            axios.delete('/api/index/delete?file_id=' + file_id + '&Authorization='
                + this.$route.query.Authorization)
                .then(response => {
                    console.log(response);
                    this.initialize_index_page();
                }, error => {
                    console.log(error)
                })
        },
        // Generate file stat
        generate_file_stat() {
            axios.post('/api/index/file_stat_generation?account_id=' + this.account_id, {}
            ).then(response => {
                console.log(response);
                this.initialize_index_page();
            }, error => {
                console.log(error)
            })
        },

        // Choose file handler, displays file name
        choose_file_clicked(event) {
            if (event.target.files.length > 0) {
                this.file_to_upload = event.target.files[0];

                const allowed_extensions = ['jpg', 'jpeg', 'png', 'pdf', 'xls', 'xlsx'];
                // Get the extension of the file to upload
                const cur_file_extension = this.file_to_upload.name.substring(this.file_to_upload.name.lastIndexOf('.') + 1).toLowerCase();
                // console.log(cur_file_extension)

                // If file type is accepted, change the choose_file_message to the filename, and file_to_upload to this file
                // Otherwise, display "Unaccepted file format"
                if (allowed_extensions.includes(cur_file_extension)) {
                    this.choose_file_message = this.file_to_upload.name;
                } else {
                    this.choose_file_message = "Unaccepted file format";
                    this.file_to_upload = null;
                }
            } else {
                this.choose_file_message = '';
            }
        },

        // Build a form with file and file type, and send it to the server
        upload_file() {
            const form = new FormData();
            form.append('file', this.file_to_upload);
            form.append('account_id', this.account_id);

            this.upload_msg = "Uploading";

            axios.post('/api/index/upload_file', form)
                .then(response => {
                    this.upload_msg = response.data.msg;
                    this.initialize_index_page();
                    this.close_popup();
                }, error => {
                    console.log(error);
                });
        },

        // Show pop up when Upload button is clicked
        show_popup() {
            this.is_pop_up_visible = true;
        },
        // Close pop up and clear related information
        close_popup() {
            this.is_pop_up_visible = false;
            this.choose_file_message = "";
            this.file_to_upload = null;
            this.upload_msg = "";
        },


        // Authorization Validation and get basic user information
        initialize_index_page() {
            axios.post('/api/index', {}
            ).then(response => {
                console.log(response)
                this.account_id = response.data.data.user_info[0][0];
                if (response.data.data.user_info[0][2] != null) {
                    this.name = response.data.data.user_info[0][2];
                } else {
                    this.name = response.data.data.user_info[0][1];
                }

                this.administration = response.data.data.user_info[0][3];
                this.avatar_suffix = response.data.data.user_info[0][4];
                this.files = response.data.data.user_files

            }, error => {
                console.log(error);
                if (error.response.status == 302 || error.response.status == 401) {
                    this.$router.push(error.response.data.data.redirection);
                }
            })
        },

        // Example for redirection using router
        goToEditPage() {
            this.$router.push({ path: '/edit', query: { Authorization: this.$route.query.Authorization } })
        },
    }
}
</script>

<style>
.avatar {
    position: absolute;
    max-width: 130px;
    max-height: 130px;
    top: 10px;
    right: 50%;
    transform: translate(50%, 0%);
}

.generate_button {
    background-color: #5750bc;
    border: none;
    color: white;
    padding: 15px 24px;
    text-align: center;
    font-size: 24px;
    border-radius: 10px;
    position: absolute;
    top: 20%;
    left: 75%;
    transform: translate(-50%, -50%);
}

.upload_button {
    background-color: #5750bc;
    border: none;
    color: white;
    padding: 15px 24px;
    text-align: center;
    font-size: 24px;
    border-radius: 10px;
    position: absolute;
    top: 20%;
    left: 90%;
    transform: translate(-50%, -50%);
}

.choose_file_button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 320px;
    margin-left: -60px;
}

.submit_button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #fa0000;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    margin-top: -100px;
}

#fileInput {
    display: none;
    /* Hide the original file input button */
}

.popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.popup_content {
    background-color: #fff;
    padding: 150px;
    border-radius: 10px;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.page_title {
    font-family: Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    font-size: xxx-large;
}
</style>