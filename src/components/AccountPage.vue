<template>
    <div class="page_title">{{ page_title }}</div>

    <div v-if="new_user">
        <h2>Customize your avatar and nickname!</h2>

        <div class="nickname">
            <label for="nickname">Nickname </label>
            <input type="text" v-model="nickname" id="nickname" />
        </div>

        <input type="file" id="avatar_input" @change="choose_avatar_clicked" accept=".jpg, .jpeg, .png">
        <label for="avatar_input" class="choose_avatar_button">Choose Avatar</label>
        <img class="preview_avatar" v-if="avatar" :src="avatar" alt="Image" />
        <h4>{{ file_upload_message }}</h4>
        <button class="submit_button" @click="submit">Finished!</button>
        <h3 style="margin-top: 40%;">{{ submit_message }}</h3>
    </div>
    <div v-else>
        <button class="login_button" @click="toggle_popup_login">Login</button>
        <button class="signup_button" @click="toggle_popup_signup">Sign up</button>

        <transition name="fade">
            <div v-if="is_popup_visible" class="popup" @click.self="closePopup">
                <div class="popup_content">
                    <div class="form_group">
                        <label for="username">Username </label>
                        <input type="text" name="username" id="username" v-model="username" @keyup.enter="enter_handler" />
                    </div>
                    <div class="form_group">
                        <label for="password">Password </label>
                        <input type="password" name="password" id="password" v-model="password"
                            @keyup.enter="enter_handler" />
                    </div>
                    <div style="font-size: medium; color: red;">{{ warning }}</div>
                    <div v-if="login_pressed"><button class="popup_button" @click="login">Login</button></div>
                    <div v-else><button class="popup_button" @click="signup">Sign up</button></div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import SHA256 from 'crypto-js/sha256';
import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5000/api/account';


export default {
    data() {
        return {
            page_title: "Welcome!",
            is_popup_visible: false,
            login_pressed: true,
            username: "",
            password: "",
            warning: "",
            new_user: false,
            account_id: 0,
            avatar: null,
            file_upload_message: "",
            nickname: "",
            submit_message: "",
            avatar_data: null,
            avatar_name: ""
        }
    },
    methods: {
        // Submit user nickname and avatar
        submit() {
            // Check empty nickname or avatar
            this.submit_message = ""
            if (this.nickname == "") {
                this.submit_message = "Empty nickname"
                return
            }
            if (this.avatar == null) {
                this.submit_message = "No avatar chosen"
                return
            }
            // Build formData
            const form = new FormData();
            form.append('avatar', this.avatar_data);
            form.append('avatar_name', this.avatar_name);
            form.append('nickname', this.nickname);
            form.append('account_id', this.account_id);

            this.submit_message = "Submitting";

            // Redirect after successful upload
            axios.post('/new_user_info', form)
                .then(response => {
                    this.submit_message = response.data.msg;
                    this.$router.push('/index');
                }, error => {
                    console.log(error);
                });

        },

        // Handle choose avatar button click event
        choose_avatar_clicked(event) {
            // Get the input file
            const file = event.target.files[0];
            this.file_upload_message = "";
            this.avatar = null;
            this.avatar_name = file.name
            if (file) {
                // Check if file suffix satisfy the requiremnet
                if (['image/jpg', 'image/jpeg', 'image/png'].includes(file.type)) {
                    const reader = new FileReader();

                    // Read the file and convert it to a data URL
                    reader.readAsDataURL(file);

                    // Handle the 'load' event when the file is read
                    reader.onload = () => {
                        this.avatar = reader.result;
                        this.avatar_data = reader.result.split(',')[1];
                    };
                } else {
                    this.file_upload_message = "Invalid file type";
                }
            }
        },

        // Handle enter pressed when user is in input box
        enter_handler() {
            if (this.login_pressed) {
                this.login()
            } else {
                this.signup()
            }
        },
        // Show login window when login is clicked
        toggle_popup_login() {
            this.is_popup_visible = true;
            this.login_pressed = true
        },
        // Show signup window when signup is clicked
        toggle_popup_signup() {
            this.is_popup_visible = true;
            this.login_pressed = false
        },
        // Close the pop up window and clear the input
        closePopup() {
            this.is_popup_visible = false;
            this.username = "";
            this.password = "";
            this.warning = "";
        },

        // Check for empty username and password
        check_empty() {
            this.warning = ""
            if (this.username == "") {
                return "Username can not be empty"
            }
            if (this.password == "") {
                return "Password can not be empty"
            }
            return ""
        },
        login() {
            // Check if input is empty
            if (this.check_empty() != "") {
                this.warning = this.check_empty()
            }
            // Send login request with the input username and password hash
            const formData = new FormData();
            formData.append('username', this.username);
            formData.append('password_hash', SHA256(this.password).toString());
            axios.post('/login', formData)
                .then(response => {
                    this.$router.push(response.data.data.url);
                }, error => {
                    this.warning = error.response.data.msg;
                    console.log(error);
                });
        },
        signup() {
            // Check if input is empty
            if (this.check_empty() != "") {
                this.warning = this.check_empty()
            }
            // Send signup request with the input username and password hash
            const formData = new FormData();
            formData.append('username', this.username);
            formData.append('password_hash', SHA256(this.password).toString());
            axios.post('/signup', formData)
                .then(response => {
                    console.log(response)
                    this.new_user = true
                    this.account_id = response.data.data.account_id
                }, error => {
                    this.warning = error.response.data.msg;
                    console.log(error);
                });
        }
    }
}
</script>

<style>
.submit_button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    font-size: 24px;
    border-radius: 4px;
    position: absolute;
    top: 75%;
    transform: translate(-50%, -50%);
}

.nickname {
    position: relative;
    margin-top: 60px;
}

.preview_avatar {
    position: absolute;
    max-width: 200px;
    max-height: 200px;
    margin-top: 50px;
}

.choose_avatar_button {
    position: absolute;
    margin-top: 400px;
    margin-left: -300px;
    display: inline-block;
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}

#avatar_input {
    display: none;
}

.form_group {
    position: relative;
    margin-bottom: 20px;
}

label {
    position: absolute;
    top: -10px;
    /* left: 10px; */
    font-weight: bold;
}

input {
    padding: 8px;
    margin-top: 10px;
}

.page_title {
    font-family: Helvetica, Arial, sans-serif;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    font-size: xxx-large;
}

.login_button {
    background-color: #5750bc;
    border: none;
    color: white;
    padding: 15px 42px;
    text-align: center;
    font-size: 40px;
    border-radius: 10px;
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
}


.login_button:hover {
    background-color: #433ac5;
}

.signup_button {
    background-color: #5750bc;
    border: none;
    color: white;
    padding: 15px 24px;
    text-align: center;
    font-size: 40px;
    border-radius: 10px;
    position: absolute;
    top: 55%;
    left: 50%;
    transform: translate(-50%, -50%);
}


.signup_button:hover {
    background-color: #433ac5;
}

.popup_button {
    background-color: #276bff;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    font-size: 16px;
    /* position: absolute;
  top: 61%;
  left: 50%;
  transform: translate(-50%, -50%); */
    position: relative;
    margin-top: 10px;
    margin-left: 25%;
    border-radius: 8px;
}

.popup_button:hover {
    background-color: #1c5be5;
}

.t2 {
    text-align: center;
    font-size: xx-large;
}

.popup {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.popup_content {
    background-color: #fff;
    padding: 60px;
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
</style>