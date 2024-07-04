import axios from "axios";
import React, { useEffect, useState } from "react";
import Modal from "react-modal";
import {Tooltip} from 'react-tooltip'
import { PersonAdd, Trash, PencilSquare, Lock } from "react-bootstrap-icons";
import FileUpload from "./FileUpload";
import ProcessFile from "./ProcessFile";
import LockScreen from "./LockScreen";

axios.defaults.withCredentials = true;

export default function ExcludedClients() {
  const [clientData, setClientData] = useState([]);
  const [name, setName] = useState("");
  const [modalIsOpen, setIsOpen] = useState(false);
  const [lockModalIsOpen, setIsOpenLock] = useState(true);
  const [updateModalIsOpen, setUpdateModalIsOpen] = useState(false);
  const [excludedList, setExcludedList] = useState([]);
  const [nameError, setNameError] = useState(null);
  
  const apiURL = "http://127.0.0.2:8000/reporting/excluded_clients/";

  // Fetch excluded client data
  useEffect(() => {
    fetch(apiURL)
      .then((response) => response.json())
      .then((fetchedData) => setExcludedList(fetchedData));
  }, []);

  const validateName = (name) => {
    setNameError(null); 

    if (!name.trim()) {
      setNameError("Please enter a client name.");
      return false;
    }
    return true;
  };

  // Function to capitalize the first letter of the name and the surname
  function capitalizeName(name) {
    let nameArray = name.split(" ");
    for (let i = 0; i < nameArray.length; i++) {
      nameArray[i] = nameArray[i].charAt(0).toUpperCase() + nameArray[i].slice(1);
    }
    return nameArray.join(" ");
  }

  // Add a client to the database
  const postData = async (e) => {
    e.preventDefault();
    if (!validateName(name)) {
      return; 
    }
    try {
      const response = await fetch(apiURL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: capitalizeName(name),
        }),
      });
      const data = await response.json();
      setExcludedList([...excludedList, data]);
      setIsOpen(false);
    } catch (error) {
      console.error(error);
    }
  };

  // Update a client in the database
  const handleDataUpdate = async (e, client_id) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiURL}${client_id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: capitalizeName(name),
        }),
      });
      const data = await response.json();

      // Update specific client in state
      const updatedList = [...excludedList];
      const clientIndex = updatedList.findIndex((client) => client.id === client_id);
      updatedList[clientIndex] = data;
      setExcludedList(updatedList);

      // Close modal on success
      setUpdateModalIsOpen(false);
    } catch (error) {
      console.error(error);
    }
  };

  function toggleModal() {
    setIsOpen(true);
  }

  function updateModal(client_id) {
    console.log(client_id)
    setClientData(excludedList.find((client) => client.id === client_id));
    setUpdateModalIsOpen(true);
  }

  //delete the client using axios
  const deleteClient = async (client_id) => {
    if (window.confirm('Are you sure you want to delete this client?')) {
      try {
        await axios.delete(`${apiURL}${client_id}`);
        const updatedList = excludedList.filter(client => client.id !== client_id);
        setExcludedList(updatedList);
      } catch (error) {
        console.error(error);
      }
    }
  };

  // Modal custom style
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
    <div className='d-flex justify-content-between'>
        <div className="col-9 d-flex flex-column">
            <header className="header p-2 d-flex align-items-center">
                <Lock color="white" width='2.5%' size='' className="lock" onClick={()=>{setIsOpenLock(true)}}/>
                <Tooltip anchorSelect=".lock" place='bottom'>
                    Lock Screen
                </Tooltip>
                <h2 className="px-2">Filter Tool</h2>
            </header>
            <div className="d-flex aling-items-center justify-content-center w-100">
                <FileUpload/>
            </div>
        </div>
      <div className="excluded col-3  borde bg-dark ">
        <div className="d-flex title justify-content-between align-items-center p-3">
          <h4>Excluded Clients</h4>
          <button
            className="btn btn-sm btn-primary"
            onClick={toggleModal}
          >
            <i><PersonAdd /></i>
            <span className="px-2">add</span>
          </button>
        </div>
        <ul className="list-unstyled m-1 p-2">
          {excludedList.map((client) => (
            <li key={client.id} className="d-flex justify-content-between client p-2">
              <small>{client.name}</small>
              <span>
                    <small className="edit-tooltip icon" onClick={() => updateModal(client.id)}>
                        <PencilSquare/>
                    </small>
                    <Tooltip anchorSelect=".edit-tooltip" place="bottom">
                        Edit client
                    </Tooltip> 
                    <small className="px-2 icon delete-tooltip" onClick={() => deleteClient(client.id)}>
                        <Trash />
                    </small>
                    <Tooltip anchorSelect=".delete-tooltip" place="bottom">
                        Delete Client
                    </Tooltip> 
              </span>
            </li>
          ))}
        </ul>
      </div>
      
      {/* Modal for adding a client */}
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={toggleModal}
        style={customStyles}
      >
        <form onSubmit={postData}>
          <div className='d-flex justify-content-center'>
            <button type='button' onClick={(e) => setIsOpen(!modalIsOpen)} className='btn btn-close'></button>
          </div>
          <h5 className="py-3">Enter Full Name of the Client</h5>
          <input
            type="text"
            className="form-control"
            placeholder="Client Name"
            onChange={(e) => setName(e.target.value)}
          />
          {nameError && <p className="text-danger">{nameError}</p>}
          <div className="py-3">
            <button className="btn btn-sm btn-primary w-100">Submit</button>
          </div>
        </form>
      </Modal>

      {/* Modal for editing a client */}
      <Modal
        isOpen={updateModalIsOpen}
        onRequestClose={updateModal}
        style={customStyles}
      >
        <form onSubmit={(e) => handleDataUpdate(e, clientData.id)}>
          <div className='d-flex justify-content-center'>
            <button type='button' onClick={(e) => setUpdateModalIsOpen(!updateModalIsOpen)} className='btn btn-close'></button>
          </div>
          <h5 className="py-3">Edit Client Name</h5>
          <input
            type="text"
            className="form-control"
            placeholder="Client Name"
            onChange={(e) => setName(e.target.value)}
            defaultValue={clientData.name}
          />
          <div className="py-3">
          {nameError && <p className="text-danger">{nameError}</p>}
            <button className="btn btn-sm btn-primary w-100">Save Changes</button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={lockModalIsOpen}
        style={customStyles}
      >
        <LockScreen setIsOpenLock={setIsOpenLock}/>
      </Modal>

    </div>
  );
}
