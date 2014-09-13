window.fbAsyncInit = function() {
 FB.init({
 appId      : '693517617401481', xfbml      : true, version    : 'v2.1' });
 start();
 };
 (function(d, s, id){
  var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {
    return;
 } js = d.createElement(s);
 js.id = id;
 js.src = "//connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));
   function showSuccessToast() {
    $().toastmessage('showSuccessToast', "Success! Check your FB Post");
 };
 function showStickySuccessToast() {
  $().toastmessage('showToast', {
  text     : 'Success Dialog which is sticky', sticky   : true, position : 'top-right', type     : 'success', closeText: '', close    : function () {
  console.log("toast is closed ...");
 } });
 };
  function showNoticeToast() {
   $().toastmessage('showNoticeToast', "Notice  Please Login");
 };
  function showStickyNoticeToast() {
   $().toastmessage('showToast', {
   text     : 'Notice Dialog which is sticky', sticky   : true, position : 'top-right', type     : 'notice', closeText: '', close    : function () {
    console.log("toast is closed ...");
} });
 };
  function showWarningToast() {
   $().toastmessage('showWarningToast', "Oh Snap!.. There's something wrong :X ");
 };
 function showStickyWarningToast() {
  $().toastmessage('showToast', {
  text     : 'Warning Dialog which is sticky', sticky   : true, position : 'top-right', type     : 'warning', closeText: '', close    : function () {
  console.log("toast is closed ...");
 } });
 };
  function showErrorToast() {
   $().toastmessage('showErrorToast', "Error Dialog which is fading away ...");
 };
 function showStickyErrorToast() {
  $().toastmessage('showToast', {
  text     : 'Error Dialog which is sticky', sticky   : true, position : 'top-right', type     : 'error', closeText: '', close    : function () {
  console.log("toast is closed ...");
 } });
 };
  function start() {
   var user;
 var baseUrl = "https://graph.facebook.com/v2.1/";
 getLoginStatus();
 $("#fb-login").click(function(){
  getLoginStatus(login);
 });
 $("#fb-logout").click(logout);
 $("#postmessage").submit(function(){
  if(user){
  var msg = $("#message").val();
 postToFB(msg);
 return false;
 }else{
  showNoticeToast();
 return false;
 } });
  function getLoginStatus(callback){
   FB.getLoginStatus(function(response){
   if(response.status=="connected"){
   getFBresponse(response);
 toggleLogin();
 }else if(typeof callback === 'function' && callback()){
  callback(response);
 } });
 };
  function postToFB(msg){
   var url = baseUrl + user.userID + "/feed/";
 var data = {
  method: "post", message: msg, access_token: user.accessToken };
 $.get(url,data,function(response){
  if(response.id){
  showSuccessToast();
 var msg = $("#post-form textarea").val("");
 }else{
  showWarningToast();
 } });
 };
 function getFBresponse(response){
  user=response.authResponse;
 };
  function login(){
   FB.login(function(response){
   if(response.authResponse){
   getFBresponse(response);
 toggleLogin();
 } }, {
    scope: 'publish_actions',return_scopes:true});
 };
  function logout(){
   FB.logout(function(){
   toggleLogin();
 user=null;
 });
 };
  function toggleLogin(){
   $("#fb-login,#fb-logout").toggle();
 };
 };
