import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import Modal from "react-modal";
import { FiletypeCsv } from "react-bootstrap-icons";
import ProcessFile from './ProcessFile';

function FileUpload() {
  const [modalIsOpen, setIsOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone();

  const isButtonDisabled = acceptedFiles.length === 0; // Concise disabled state logic

  const handleSubmitFile = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const file = acceptedFiles[0];
    const fileExtension = file.name.split('.').pop();

    console.log('here');

    // Check if extension is "csv"
    if (fileExtension === "csv") {
      setSelectedFile(file);
      console.log("Valid CSV file selected!");
    } else {
      console.log("Invalid file type. Please upload a CSV file.");
      setSelectedFile(null);
      return;
    }

    formData.append('file', selectedFile);
    console.log(formData, selectedFile);

    try {
      const response = await fetch('http://127.0.0.2:8000/reporting/raw_csv_files/', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        console.log('File uploaded successfully!');
        setIsOpen(true);
      } else {
        alert('Error uploading file');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const files = acceptedFiles.map(file => (
    <p key={file.path} className='p-2 text-light bg-secondary '>
      <FiletypeCsv className='text-success' />
      <span className='px-2'>{file.path} - {file.size} bytes</span>
    </p>
  ));

  function toggleModal() {
    setIsOpen(true);
  }

  const customStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
    },
  };

  return (
    <>
      <div className='file-drop d-flex align-items-center'>
        <div className="contanier border p-5">
          <div {...getRootProps({ className: 'dropzone' })}>
            <input {...getInputProps()} />
            <p className='text-center'>Drag 'n' drop a file here, or click to select file</p>
          </div>
          <div>
            {files}
          </div>
          <form onSubmit={handleSubmitFile} className='px-2'>
            {/* Use disabled prop based on isButtonDisabled */}
            <button type="submit" className='btn btn-primary w-100' disabled={isButtonDisabled}>
              Upload
            </button>
          </form>
        </div>
      </div>
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={toggleModal}
        style={customStyles}
      >
        <ProcessFile setIsOpen={setIsOpen} modalIsOpen={modalIsOpen} />
      </Modal>
    </>
  );
}

export default FileUpload;
