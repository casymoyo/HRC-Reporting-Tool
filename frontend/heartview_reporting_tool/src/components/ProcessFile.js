import React from 'react';

export default function ProcessFile( { modalIsOpen, setIsOpen }) {

  const handleClick = () => {
    setIsOpen(false)
  };

  return (
    <a href='http://127.0.0.2:8000/reporting/process' onClick={handleClick} className='btn btn-success btn-lg'>
      Process and Download File
    </a>
  );
}

