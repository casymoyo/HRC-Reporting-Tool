import React, {useState} from 'react'
import Modal from "react-modal";
import axios from 'axios';

export default function LockScreen({setIsOpenLock}) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const login = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.2:8000/users/login/', {
        username,
        password,
      });
      const { token } = response.data;
      // Store the token in local storage or secure cookie
      localStorage.setItem('token', token);
      setIsOpenLock(false)
      return true;
    } catch (error) {
      console.error(error);
      return false;
    }
  };


  return (
    <div>
        <form className='p-5' onSubmit={login}>
            <h2>Your Crecedentials Please :)</h2>
            <div className='row mb-2 mt-2'>
                <input
                    type='text'
                    placeholder='username'
                    className='form-control'
                    onChange={(e)=>{setUsername(e.target.value)}}
                ></input>
            </div>
            <div className='row mb-2'>
                <input
                    type='password'
                    placeholder='password'
                    className='form-control'
                    onChange={(e)=>{setPassword(e.target.value)}}
                ></input>
            </div>
            <div className='row'>
                <button className='btn btn-primary'>Unlock</button>
            </div>
        </form>
    </div>
  )
}
