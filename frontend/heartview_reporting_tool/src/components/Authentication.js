import axios from 'axios';

    const API_URL = 'http://127.0.0.2:8000/users/login/';

    function login(username, password) {
      return axios.post(API_URL + 'token/', {
        username,
        password
      })
      .then(response => {
        if (response.data.access) {
          localStorage.setItem('user', JSON.stringify(response.data));
        }
        return response.data;
      });
    }
    
    function logout() {
      localStorage.removeItem('user');
    }
    
    function getCurrentUser() {
      return JSON.parse(localStorage.getItem('user'));
    }
    
    export default {
      login,
      logout,
      getCurrentUser
    };


