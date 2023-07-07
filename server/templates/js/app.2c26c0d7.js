(function(){var e={5385:function(e,t,i){"use strict";var a=i(9242),o=i(3396);const n={id:"app"};function s(e,t,i,a,s,r){const u=(0,o.up)("router-view");return(0,o.wg)(),(0,o.iD)("div",n,[(0,o.Wm)(u)])}var r={name:"App"},u=i(89);const l=(0,u.Z)(r,[["render",s]]);var p=l,_=i(2483),d=i(7139);const c={key:0},h={class:"page_title"},g={key:0},f=(0,o._)("h2",null,"Customize your avatar and nickname!",-1),m={class:"nickname"},v=(0,o._)("label",{for:"nickname"},"Nickname ",-1),w=(0,o._)("label",{for:"avatar_input",class:"choose_avatar_button"},"Choose Avatar",-1),b=["src"],y={style:{"margin-top":"-400px"}},k={style:{"margin-top":"40%"}},z={key:1},x={style:{color:"red"}},q={class:"popup_content"},$={class:"form_group"},D=(0,o._)("label",{for:"username"},"Username ",-1),C={class:"form_group"},A=(0,o._)("label",{for:"password"},"Password ",-1),Z={style:{"font-size":"medium",color:"red"}},U={key:0},j={key:1};function P(e,t,i,n,s,r){return null==s.authorization_token||s.new_user?((0,o.wg)(),(0,o.iD)("div",c,[(0,o._)("div",h,(0,d.zw)(s.page_title),1),s.new_user?((0,o.wg)(),(0,o.iD)("div",g,[f,(0,o._)("div",m,[v,(0,o.wy)((0,o._)("input",{type:"text","onUpdate:modelValue":t[0]||(t[0]=e=>s.nickname=e),id:"nickname"},null,512),[[a.nr,s.nickname]])]),(0,o._)("input",{type:"file",id:"avatar_input",onChange:t[1]||(t[1]=(...e)=>r.choose_avatar_clicked&&r.choose_avatar_clicked(...e)),accept:".jpg, .jpeg, .png"},null,32),w,s.avatar?((0,o.wg)(),(0,o.iD)("img",{key:0,class:"preview_avatar",src:s.avatar,alt:"Image"},null,8,b)):(0,o.kq)("",!0),(0,o._)("h4",y,(0,d.zw)(s.file_upload_message),1),(0,o._)("button",{class:"submit_button",onClick:t[2]||(t[2]=(...e)=>r.submit&&r.submit(...e))},"Finished!"),(0,o._)("h3",k,(0,d.zw)(s.submit_message),1)])):((0,o.wg)(),(0,o.iD)("div",z,[(0,o._)("button",{class:"login_button",onClick:t[3]||(t[3]=(...e)=>r.toggle_popup_login&&r.toggle_popup_login(...e))},"Login"),(0,o._)("button",{class:"signup_button",onClick:t[4]||(t[4]=(...e)=>r.toggle_popup_signup&&r.toggle_popup_signup(...e))},"Sign up"),(0,o._)("h2",x,(0,d.zw)(s.account_warning_msg),1),(0,o.Wm)(a.uT,{name:"fade"},{default:(0,o.w5)((()=>[s.is_popup_visible?((0,o.wg)(),(0,o.iD)("div",{key:0,class:"popup",onClick:t[11]||(t[11]=(0,a.iM)(((...e)=>r.closePopup&&r.closePopup(...e)),["self"]))},[(0,o._)("div",q,[(0,o._)("div",$,[D,(0,o.wy)((0,o._)("input",{type:"text",name:"username",id:"username","onUpdate:modelValue":t[5]||(t[5]=e=>s.username=e),onKeyup:t[6]||(t[6]=(0,a.D2)(((...e)=>r.enter_handler&&r.enter_handler(...e)),["enter"]))},null,544),[[a.nr,s.username]])]),(0,o._)("div",C,[A,(0,o.wy)((0,o._)("input",{type:"password",name:"password",id:"password","onUpdate:modelValue":t[7]||(t[7]=e=>s.password=e),onKeyup:t[8]||(t[8]=(0,a.D2)(((...e)=>r.enter_handler&&r.enter_handler(...e)),["enter"]))},null,544),[[a.nr,s.password]])]),(0,o._)("div",Z,(0,d.zw)(s.warning),1),s.login_pressed?((0,o.wg)(),(0,o.iD)("div",U,[(0,o._)("button",{class:"popup_button",onClick:t[9]||(t[9]=(...e)=>r.login&&r.login(...e))},"Login")])):((0,o.wg)(),(0,o.iD)("div",j,[(0,o._)("button",{class:"popup_button",onClick:t[10]||(t[10]=(...e)=>r.signup&&r.signup(...e))},"Sign up")]))])])):(0,o.kq)("",!0)])),_:1})]))])):(0,o.kq)("",!0)}i(7658);var O=i(9002),F=i.n(O),I=i(4161);I.Z.defaults.baseURL="http://127.0.0.1:5000";var T={data(){return{page_title:"Welcome!",is_popup_visible:!1,login_pressed:!0,username:"",password:"",warning:"",new_user:!1,account_id:0,avatar:null,file_upload_message:"",nickname:"",submit_message:"",avatar_data:null,avatar_name:"",account_warning_msg:"",authorization_token:""}},mounted(){""!=this.$route.query.Authorization&&(this.authorization_token=this.$route.query.Authorization,I.Z.defaults.headers.common["Authorization"]=this.$route.query.Authorization,this.initialize_account_page()),this.account_warning_msg=this.$route.query.warning},methods:{initialize_account_page(){I.Z.post("/api/account?redirection="+this.$route.query.redirection+"&file_id="+this.$route.query.file_id).then((e=>{console.log(e),"Authorized"==e.data.msg&&this.$router.push({path:this.$route.query.redirection,query:{file_id:this.$route.query.file_id,Authorization:e.data.data.token}})}),(e=>{console.log(e)}))},submit(){if(this.submit_message="",""==this.nickname)return void(this.submit_message="Empty nickname");if(null==this.avatar)return void(this.submit_message="No avatar chosen");const e=new FormData;e.append("avatar",this.avatar_data),e.append("avatar_name",this.avatar_name),e.append("nickname",this.nickname),e.append("account_id",this.account_id),this.submit_message="Submitting",I.Z.post("/api/account/new_user_info",e).then((e=>{this.submit_message=e.data.msg,this.$router.push({path:"/index",query:{Authorization:this.authorization_token}})}),(e=>{console.log(e)}))},choose_avatar_clicked(e){const t=e.target.files[0];if(this.file_upload_message="",this.avatar=null,this.avatar_name=t.name,t)if(["image/jpg","image/jpeg","image/png"].includes(t.type)){const e=new FileReader;e.readAsDataURL(t),e.onload=()=>{this.avatar=e.result,this.avatar_data=e.result.split(",")[1]}}else this.file_upload_message="Invalid file type"},enter_handler(){this.login_pressed?this.login():this.signup()},toggle_popup_login(){this.is_popup_visible=!0,this.login_pressed=!0},toggle_popup_signup(){this.is_popup_visible=!0,this.login_pressed=!1},closePopup(){this.is_popup_visible=!1,this.username="",this.password="",this.warning=""},check_empty(){return this.warning="",""==this.username?"Username can not be empty":""==this.password?"Password can not be empty":""},login(){if(""!=this.check_empty())return void(this.warning=this.check_empty());const e=new FormData;e.append("username",this.username),e.append("password_hash",F()(this.password).toString()),I.Z.post("/api/account/login",e).then((e=>{console.log(e),this.$router.push({path:e.data.data.redirection,query:{Authorization:e.data.data.token}})}),(e=>{this.warning=e.response.data.msg,console.log(e)}))},signup(){if(""!=this.check_empty())return void(this.warning=this.check_empty());const e=new FormData;e.append("username",this.username),e.append("password_hash",F()(this.password).toString()),I.Z.post("/api/account/signup",e).then((e=>{console.log(e),this.new_user=!0,this.account_id=e.data.data.account_id,this.authorization_token=e.data.data.token}),(e=>{this.warning=e.response.data.msg,console.log(e)}))}}};const E=(0,u.Z)(T,[["render",P]]);var L=E;const R={style:{"text-align":"right"}},S={class:"page_title"},W={class:"popup_content"},K=(0,o._)("label",{for:"fileInput",class:"choose_file_button"},"Choose File",-1),M={key:0},V=["href"],H={style:{float:"right"}};function N(e,t,i,n,s,r){return(0,o.wg)(),(0,o.iD)(o.HY,null,[(0,o._)("h3",R,"Welcome, "+(0,d.zw)(s.name),1),(0,o._)("div",S,(0,d.zw)(s.page_title),1),(0,o._)("button",{onClick:t[0]||(t[0]=(...e)=>r.goToEditPage&&r.goToEditPage(...e))},"Go To Edit Page"),(0,o._)("button",{class:"upload_button",onClick:t[1]||(t[1]=(...e)=>r.show_popup&&r.show_popup(...e))},"Upload"),(0,o.Wm)(a.uT,{name:"fade"},{default:(0,o.w5)((()=>[s.is_pop_up_visible?((0,o.wg)(),(0,o.iD)("div",{key:0,class:"popup",onClick:t[4]||(t[4]=(0,a.iM)(((...e)=>r.close_popup&&r.close_popup(...e)),["self"]))},[(0,o._)("div",W,[(0,o._)("input",{type:"file",id:"fileInput",onChange:t[2]||(t[2]=(...e)=>r.choose_file_clicked&&r.choose_file_clicked(...e)),accept:".jpg, .jpeg, .png, .pdf, .xls .xlsx"},null,32),K,(0,o._)("p",null,(0,d.zw)(s.choose_file_message),1),""!=s.choose_file_message&&"Unaccepted file format"!=s.choose_file_message?((0,o.wg)(),(0,o.iD)("div",M,[(0,o._)("button",{class:"submit_button",onClick:t[3]||(t[3]=(...e)=>r.upload_file&&r.upload_file(...e))},"Submit"),(0,o._)("p",null,(0,d.zw)(s.upload_msg),1)])):(0,o.kq)("",!0)])])):(0,o.kq)("",!0)])),_:1}),(0,o._)("ol",null,[((0,o.wg)(!0),(0,o.iD)(o.HY,null,(0,o.Ko)(s.files,(e=>((0,o.wg)(),(0,o.iD)("li",{key:e},[(0,o._)("a",{href:`/edit?file_id=${encodeURIComponent(e[0])}&Authorization=${this.$route.query.Authorization}`,target:"_blank",style:{float:"left"}},(0,d.zw)(e[2]),9,V),(0,o._)("span",H,(0,d.zw)(e[4]),1)])))),128))])],64)}I.Z.defaults.baseURL="http://127.0.0.1:5000";var Y={data(){return{page_title:"Index Page",account_id:0,name:"",administration:0,avatar_suffix:"",files:null,is_pop_up_visible:!1,choose_file_message:"",upload_msg:"",file_to_upload:null}},mounted(){I.Z.defaults.headers.common["Authorization"]=this.$route.query.Authorization,this.initialize_index_page()},methods:{file_edit_page_link(e){return"/edit?filename=${encodeURIComponent(file)}"+e+"ad"},choose_file_clicked(e){if(e.target.files.length>0){this.file_to_upload=e.target.files[0];const t=["jpg","jpeg","png","pdf","xls","xlsx"],i=this.file_to_upload.name.substring(this.file_to_upload.name.lastIndexOf(".")+1).toLowerCase();t.includes(i)?this.choose_file_message=this.file_to_upload.name:(this.choose_file_message="Unaccepted file format",this.file_to_upload=null)}else this.choose_file_message=""},upload_file(){const e=new FormData;e.append("file",this.file_to_upload),e.append("account_id",this.account_id),this.upload_msg="Uploading",I.Z.post("/api/index/upload_file",e).then((e=>{this.upload_msg=e.data.msg,this.initialize_index_page(),this.close_popup()}),(e=>{console.log(e)}))},show_popup(){this.is_pop_up_visible=!0},close_popup(){this.is_pop_up_visible=!1,this.choose_file_message="",this.file_to_upload=null,this.upload_msg=""},initialize_index_page(){I.Z.post("/api/index",{}).then((e=>{console.log(e),this.account_id=e.data.data.user_info[0][0],null!=e.data.data.user_info[0][2]?this.name=e.data.data.user_info[0][2]:this.name=e.data.data.user_info[0][1],this.administration=e.data.data.user_info[0][3],this.avatar_suffix=e.data.data.user_info[0][4],this.files=e.data.data.user_files}),(e=>{console.log(e),302!=e.response.status&&401!=e.response.status||this.$router.push(e.response.data.data.redirection)}))},goToEditPage(){this.$router.push({path:"/edit",query:{Authorization:this.$route.query.Authorization}})}}};const G=(0,u.Z)(Y,[["render",N]]);var B=G;const J={class:"page_title"};function Q(e,t,i,a,n,s){return(0,o.wg)(),(0,o.iD)("div",J,(0,d.zw)(n.page_title),1)}I.Z.defaults.baseURL="http://127.0.0.1:5000";var X={data(){return{page_title:"Edit Page",file_id:null}},mounted(){I.Z.defaults.headers.common["Authorization"]=this.$route.query.Authorization,this.initialize_edit_page()},methods:{initialize_edit_page(){this.file_id=this.$route.query.file_id,I.Z.post("/api/edit?file_id="+this.file_id,{}).then((e=>{console.log(e)}),(e=>{console.log(e),302!=e.response.status&&401!=e.response.status||this.$router.push(e.response.data.data.redirection)}))}}};const ee=(0,u.Z)(X,[["render",Q]]);var te=ee;const ie=[{path:"/",redirect:"/index"},{path:"/account",component:L},{path:"/index",component:B},{path:"/edit",component:te}],ae=(0,_.p7)({history:(0,_.PO)(),routes:ie});var oe=ae;(0,a.ri)(p).use(oe).mount("#app")},2480:function(){}},t={};function i(a){var o=t[a];if(void 0!==o)return o.exports;var n=t[a]={exports:{}};return e[a].call(n.exports,n,n.exports,i),n.exports}i.m=e,function(){var e=[];i.O=function(t,a,o,n){if(!a){var s=1/0;for(p=0;p<e.length;p++){a=e[p][0],o=e[p][1],n=e[p][2];for(var r=!0,u=0;u<a.length;u++)(!1&n||s>=n)&&Object.keys(i.O).every((function(e){return i.O[e](a[u])}))?a.splice(u--,1):(r=!1,n<s&&(s=n));if(r){e.splice(p--,1);var l=o();void 0!==l&&(t=l)}}return t}n=n||0;for(var p=e.length;p>0&&e[p-1][2]>n;p--)e[p]=e[p-1];e[p]=[a,o,n]}}(),function(){i.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return i.d(t,{a:t}),t}}(),function(){i.d=function(e,t){for(var a in t)i.o(t,a)&&!i.o(e,a)&&Object.defineProperty(e,a,{enumerable:!0,get:t[a]})}}(),function(){i.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){i.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={143:0};i.O.j=function(t){return 0===e[t]};var t=function(t,a){var o,n,s=a[0],r=a[1],u=a[2],l=0;if(s.some((function(t){return 0!==e[t]}))){for(o in r)i.o(r,o)&&(i.m[o]=r[o]);if(u)var p=u(i)}for(t&&t(a);l<s.length;l++)n=s[l],i.o(e,n)&&e[n]&&e[n][0](),e[n]=0;return i.O(p)},a=self["webpackChunkpersonal_file_storage"]=self["webpackChunkpersonal_file_storage"]||[];a.forEach(t.bind(null,0)),a.push=t.bind(null,a.push.bind(a))}();var a=i.O(void 0,[998],(function(){return i(5385)}));a=i.O(a)})();
//# sourceMappingURL=app.2c26c0d7.js.map