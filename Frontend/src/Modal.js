import { motion } from "framer-motion";
import Backdrop from "./Backdrop";
import { useState } from "react";

const dropIn = {
    hidden: {
        y: "-100vh",
        opacity: 0,
    },
    visible: {
        y: "0",
        opacity: 1,
        transition: {
            duration: 0.1,
            type: "spring",
            damping: 25,
            stiffness: 500,
        },
    },
    exit: {
        y: "100vh",
        opacity: 0,
    },
};


const Modal = ({ handleClose, imageUrl }) => {

    const [file, setFile] = useState(null);
    // eslint-disable-next-line
    const [result, setResult] = useState(null);


    const handleFileChange = (e) => {
        if (e.target.files.length !== 0) {
            const data = new FileReader();
            data.addEventListener('load', () => {
                setFile(data.result)
            })
            //   console.log(file)
            data.readAsDataURL(e.target.files[0])

        }


    }

    const handleSubmit = () => {
        console.log(imageUrl)
    }


    return (
        <Backdrop onClick={handleClose}>
            <motion.div
                onClick={(e) => e.stopPropagation()}
                className="modal orange-gradient"
                variants={dropIn}
                initial="hidden"
                animate="visible"
                exit="exit"
            >
                <span onClick={handleClose} className="closeBtn material-symbols-outlined">Close</span>

                <div className="imageGallery">
                    <div className="chatImage">
                        <img alt="fashion-img" src={imageUrl} />

                    </div>
                    <div className="material-symbols-outlined add icon">add</div>
                    <div className="chatImage">
                        {
                            file === null ?
                                <div className="uploadImage">
                                    <input type="file" id="photo-upload" onChange={handleFileChange} />
                                    <motion.label
                                        htmlFor="photo-upload"
                                        className="uploadImageBtn"
                                        // onClick={displayChatBot}
                                        whileHover={{ scale: 1.1 }}
                                        whileTap={{ scale: 0.9 }}
                                    >
                                        Photo
                                    </motion.label>
                                </div>
                                :
                                <img alt="fashion-img" src={file} />

                        }
                    </div>
                    <div className="material-symbols-outlined icon">equal</div>
                    <div className="chatImage">

                        {
                            result === null ?
                                <div className="uploadImage">
                                    <motion.label
                                        className="uploadImageBtn"
                                        onClick={handleSubmit}
                                        whileHover={{ scale: 1.1 }}
                                        whileTap={{ scale: 0.9 }}
                                    >
                                        Result
                                    </motion.label>
                                </div>
                                :
                                <img alt="fashion-img" src={result} />

                        }

                    </div>
                </div>

            </motion.div>
        </Backdrop>
    );
};


export default Modal;