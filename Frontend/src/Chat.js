import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Modal from "./Modal";
import { ThreeDots } from "react-loader-spinner";
import axios from "axios";

const Chat = () => {
    const [showChat, setShowChat] = useState(false);
    const [inputText, setInputText] = useState("");
    const [caption, setCaption] = useState("");
    const [file, setFile] = useState(null);
    const [modalOpen, setModalOpen] = useState(false);
    const [imageUrl, setImageUrl] = useState("");
    // eslint-disable-next-line
    const [loading, setLoading] = useState(false);

    // eslint-disable-next-line
    const close = (Url) => {
        setModalOpen(false);
    };
    // eslint-disable-next-line
    const open = (Url) => {
        setImageUrl(Url);
        setModalOpen(true);
    };
    const [chat, setChat] = useState([
        {
            id: 1,
            user: "bot",
            type: "text",
            message: "Hi there 👋\nHow can I help you today?",
        },
    ]);

    //display chatbot
    const displayChatBot = () => {
        setShowChat(!showChat);
    };

    //input box
    const inputChange = (e) => {
        setInputText(e.target.value);
    };
    const captionChange = (e) => {
        setCaption(e.target.value);
    };

    function timeout(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
    async function sleep(sec) {
        await timeout(sec);
        // return fn(...args);
    }

    const addMessage = async () => {
        let newMessage = {
            id: chat.length + 1,
            user: "me",
            type: "text",
            message: inputText,
        };

        setChat([...chat, newMessage]);

        const query = inputText;

        setInputText("");
        setLoading(true);

        await axios
            .post(`http://127.0.0.1:8000/predict`, {
                query: query,
            })
            .then((res) => {
                const data = res.data;
                console.log(data["products"].length)


                // array to store the image objects
                let imgarray = [];
                let idTemp = chat.length+2;
                if (data["products"].length !== 0) {

                    data["products"].forEach((product) => {
                        let name = product[0];
                        let link = product[1];
                        let img64 = product[2];
                        let imgMessage = {
                            id: idTemp,
                            user: "bot",
                            type: "image",
                            imageUrl: img64,
                            name: name,
                            link: link
                        };
                        //push each img objects
                        imgarray.push(imgMessage);
                        //update id
                        idTemp = idTemp+1;
                        // fileOutput(img64);
                    });
                    //after iteration, send all the img objects at once along with the msg
                    //if empty, np it will not get added
                    getResponse([...chat, newMessage], data["message"], imgarray);
                }
            })
            .catch(() => {
                // contact us later
                getResponse([...chat, newMessage]);
            });
    };

    const getResponse = async (chatList, message, imgarray) => {
        let newMessage = {
            id: chatList.length + 1,
            user: "bot",
            type: "text",
            message: message,
        };

        // let imgMessage = {
        //     id: chatList.length + 1,
        //     user: "bot",
        //     type: "image",
        //     imageUrl: img64,
        // };

        await sleep(2000);
        setLoading(false);
        setChat([...chatList, newMessage, imgarray]);
        // setChat([...chatList, imgMessage]);
    };

    //image upload
    const handleFileChange = (e) => {
        if (e.target.files.length !== 0) {
            const data = new FileReader();
            data.addEventListener("load", () => {
                setFile(data.result);
            });
            data.readAsDataURL(e.target.files[0]);
        }
    };

    const fileInput = () => {
        let newImage = {
            id: chat.length + 1,
            user: "me",
            type: "image",
            imageUrl: file,
        };

        setChat([...chat, newImage]);
        setFile(null);
    };

    const fileOutput = (img64) => {
        let newImage = {
            id: chat.length + 2,
            user: "bot",
            type: "image",
            imageUrl: img64,
        };

        setChat([...chat, newImage]);
    };

    return (
        <div className="chatBody">
            <AnimatePresence initial={false} onExitComplete={() => null}>
                {
                    <div className="container">
                        <div className="chatbot">
                            <header>
                                <h2>Chatbot</h2>
                            </header>

              {!showChat && (
                <div className="get-started-container">
                  <div className="separator-1">
                    <div className="trending"
                      onClick={displayChatBot}
                    >
                      <div 
                        className="trending-text"
                      >
                      Trending <br/>
                      Right <br/>
                      NOW
                      </div>
                    </div>
                    <div 
                      className="trending virtual-try-on-poster"
                      onClick={displayChatBot}
                    >
                      <div className="vtron-text">
                        Try our new <br/> Virtual <br/>Try-ON (V-TRON)
                      </div>
                    </div>
                  </div>
                  <div className="separator-2">
                    <motion.div
                      className="get-started"
                      onClick={displayChatBot}
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      Get Started
                    </motion.div>
                  </div>
                </div>
              )}

                            {file !== null && (
                                <>
                                    <div className="overlay"></div>
                                    <div className="chat-input-img">
                                        <div className="imageBox">
                                            <img alt="fashion-img" src={file} />
                                        </div>
                                        <div className="img-input-box">
                                            <input
                                                placeholder="Caption(optional)"
                                                name="img-caption"
                                                value={caption}
                                                onChange={captionChange}
                                            />
                                            <span
                                                id="send-btn"
                                                className="material-symbols-rounded"
                                                onClick={fileInput}
                                            >
                                                send
                                            </span>
                                        </div>
                                    </div>
                                </>
                            )}

                            {
                                <>
                                    <ul className="chatbox">
                                        {showChat && (
                                            <>
                                                {chat.map((message) => {
                                                    if (
                                                        message.user === "bot" &&
                                                        message.type === "text"
                                                    ) {
                                                        return (
                                                            <motion.li
                                                                initial={{ opacity: 0, scale: 0.8, height: 0 }}
                                                                animate={{
                                                                    opacity: 1,
                                                                    scale: 1,
                                                                    height: "auto",
                                                                }}
                                                                exit={{ opacity: 1, scale: 0.8, height: 0 }}
                                                                transition={{ opacity: { duration: 0.2 } }}
                                                                className="chat incoming"
                                                                key={message.id}
                                                            >
                                                                <span className="chat-toy material-symbols-outlined">
                                                                    smart_toy
                                                                </span>
                                                                <p>{message.message}</p>
                                                            </motion.li>
                                                        );
                                                    } else if (
                                                        message.user === "bot" &&
                                                        message.type === "image"
                                                    ) {
                                                        return (
                                                            <motion.li
                                                                initial={{ opacity: 0, scale: 0.8, height: 0 }}
                                                                animate={{
                                                                    opacity: 1,
                                                                    scale: 1,
                                                                    height: "auto",
                                                                }}
                                                                exit={{ opacity: 1, scale: 0.8, height: 0 }}
                                                                transition={{ opacity: { duration: 0.2 } }}
                                                                className="chat incoming virtual"
                                                                key={message.id}
                                                            >
                                                                <span className="chat-toy material-symbols-outlined">
                                                                    smart_toy
                                                                </span>
                                                                <img
                                                                    alt="fashion-img"
                                                                    src={message.imageUrl}
                                                                    className="chatImage"
                                                                />


                                                                <div className="overlay-img">
                                                                    {/* {Hello} */}
                                                                    <span>
                                                                        <a className="flipkartURL" href={message.link} target="_blank">
                                                                            {/* Men Regular Fit Checkered Spread Collar Casual Shirt(Pack of 2) */}
                                                                            {message.name}
                                                                        </a>
                                                                    </span>

                                                                </div>



                                                                <span
                                                                    className="virtual-try-on material-symbols-outlined"
                                                                    onClick={() =>
                                                                        modalOpen
                                                                            ? close(message.imageUrl)
                                                                            : open(message.imageUrl)
                                                                    }
                                                                >
                                                                    photo_camera
                                                                </span>
                                                            </motion.li>
                                                        );
                                                    } else if (
                                                        message.user === "me" &&
                                                        message.type === "image"
                                                    ) {
                                                        return (
                                                            <motion.li
                                                                initial={{ opacity: 0, scale: 0.8, height: 0 }}
                                                                animate={{
                                                                    opacity: 1,
                                                                    scale: 1,
                                                                    height: "auto",
                                                                }}
                                                                exit={{ opacity: 1, scale: 0.8, height: 0 }}
                                                                transition={{ opacity: { duration: 0.2 } }}
                                                                className="chat outgoing"
                                                                key={message.id}
                                                            >
                                                                <img
                                                                    alt="fashion-img"
                                                                    src={message.imageUrl}
                                                                    className="chatImage"
                                                                />
                                                            </motion.li>
                                                        );
                                                    }
                                                    return (
                                                        <motion.li
                                                            initial={{ opacity: 0, scale: 0.8, height: 0 }}
                                                            animate={{ opacity: 1, scale: 1, height: "auto" }}
                                                            exit={{ opacity: 1, scale: 0.8, height: 0 }}
                                                            transition={{ opacity: { duration: 0.2 } }}
                                                            className="chat outgoing"
                                                            key={message.id}
                                                        >
                                                            <p>{message.message}</p>
                                                        </motion.li>
                                                    );
                                                })}

                                                {loading && (
                                                    <motion.li
                                                        initial={{ opacity: 0, scale: 0.8, height: 0 }}
                                                        animate={{ opacity: 1, scale: 1, height: "auto" }}
                                                        exit={{ opacity: 1, scale: 0.8, height: 0 }}
                                                        transition={{ opacity: { duration: 0.2 } }}
                                                        className="chat incoming"
                                                    >
                                                        <span className="chat-toy material-symbols-outlined">
                                                            smart_toy
                                                        </span>
                                                        <div className="loading">
                                                            <ThreeDots
                                                                height="30"
                                                                width="30"
                                                                radius="9"
                                                                color="#89379c"
                                                                ariaLabel="three-dots-loading"
                                                                wrapperStyle={{}}
                                                                wrapperClassName=""
                                                                visible={true}
                                                            />
                                                        </div>
                                                    </motion.li>
                                                )}
                                            </>
                                        )}
                                    </ul>
                                    {showChat && (
                                        <>
                                            <div className="chat-input">
                                                <textarea
                                                    placeholder="Enter a message..."
                                                    value={inputText}
                                                    onChange={inputChange}
                                                />
                                                {inputText !== "" ? (
                                                    <span
                                                        id="send-btn"
                                                        className="material-symbols-outlined"
                                                        onClick={addMessage}
                                                    >
                                                        send
                                                    </span>
                                                ) : (
                                                    <>
                                                        <input
                                                            type="file"
                                                            id="file-upload"
                                                            onChange={handleFileChange}
                                                        />
                                                        <label htmlFor="file-upload">
                                                            <span
                                                                id="send-btn"
                                                                className="material-symbols-outlined"
                                                            >
                                                                image
                                                            </span>
                                                        </label>
                                                    </>
                                                )}
                                            </div>
                                        </>
                                    )}
                                </>
                            }
                        </div>

                        <motion.button
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            whileHover={{ rotate: 360, scale: 1.1 }}
                            className="chatbot-toggler"
                            onClick={displayChatBot}
                        >
                            <span className="material-symbols-outlined">close</span>
                        </motion.button>
                    </div>
                }

                {/* */}

                {modalOpen && imageUrl !== "" && (
                    <Modal
                        modalOpen={modalOpen}
                        imageUrl={imageUrl}
                        handleClose={close}
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default Chat;
