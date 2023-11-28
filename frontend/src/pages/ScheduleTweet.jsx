import { useState, useCallback } from "react";
import "./ScheduleTweet.css";
import { useDropzone } from "react-dropzone";
import DatePicker from "react-datepicker";
import toast from "react-hot-toast";
import "react-datepicker/dist/react-datepicker.css";
import {
  Button,
  Switch,
  TextField,
  FormControlLabel,
  FormGroup,
  duration,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import SendIcon from "@mui/icons-material/Send";
import DeleteForeverOutlinedIcon from "@mui/icons-material/DeleteForeverOutlined";
import { ApiConnector } from "../api/ApiConnector";

function ScheduleTweet() {
  const { postContent, postPoll, uploadImage } = ApiConnector();

  const [isPoll, setIsPoll] = useState(false);
  const [tweetText, setTweetText] = useState("");
  const [date, setDate] = useState(new Date());
  const [files, setFiles] = useState(null);
  const [pollOption1, setPollOption1] = useState("");
  const [pollOption2, setPollOption2] = useState("");
  const [pollOption3, setPollOption3] = useState("");
  const [pollOption4, setPollOption4] = useState("");
  const [pollDuration, setPollDuration] = useState(5000);

  const onDrop = useCallback((acceptedFiles) => {
    setFiles(acceptedFiles);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 4,
    accept: {
      "image/jpeg": [".jpeg", ".png"],
    },
  });

  function resetAllFields() {
    setTweetText("");
    setDate(new Date());
    setFiles(null);
    setPollOption1("");
    setPollOption2("");
    setPollOption3("");
    setPollOption4("");
    setPollDuration(0);
  }

  async function submit() {
    if (!tweetText) {
      toast.error("Tweet text is missing", {
        position: "bottom-right",
        duration: 5000,
      });
      return;
    }
    if (isPoll && !pollOption1) {
      toast.error("Poll option 1 is missing", {
        position: "bottom-right",
        duration: 5000,
      });
      return;
    }
    if (isPoll && !pollOption2) {
      toast.error("Poll option 2 is missing", {
        position: "bottom-right",
        duration: 5000,
      });
      return;
    }
    // setError(false);

    const formattedDate = `${date.getFullYear()}-${
      date.getMonth() + 1
    }-${date.getDate()}`;

    if (!isPoll) {
      const promisesArray = [];
      if (files) {
        files.forEach((file) => promisesArray.push(uploadImage(file)));
      }

      const uploadedImages = files ? await Promise.all(promisesArray) : null;

      postContent({
        text: tweetText,
        date: formattedDate,
        images: uploadedImages,
      });
    }

    if (isPoll) {
      const options = [];
      if (pollOption1) options.push(`opt1=${pollOption1}`);
      if (pollOption2) options.push(`&opt2=${pollOption2}`);
      if (pollOption3) options.push(`&opt3=${pollOption3}`);
      if (pollOption4) options.push(`&opt4=${pollOption4}`);

      postPoll({
        text: tweetText,
        options: options.join().replaceAll(",", ""),
        duration: pollDuration,
        date: formattedDate,
      });
    }

    toast.success("Tweet scheduled correctly", {
      position: "bottom-right",
      duration: 5000,
    });

    resetAllFields();
  }

  return (
    <div className="ScheduleTweet">
      <h2>SCHEDULE TWEET</h2>
      <FormGroup className="SwitchContainer">
        <FormControlLabel
          control={<Switch />}
          label="Poll"
          onChange={() => setIsPoll(!isPoll)}
        />
      </FormGroup>
      <section className="TweetTextContainer">
        <h3>Tweet text</h3>
        <textarea
          name="TweetText"
          id=""
          cols="30"
          rows="10"
          maxLength={255}
          value={tweetText}
          onChange={(event) => setTweetText(event.target.value)}
        ></textarea>
      </section>
      <section className="TweetDateContainer">
        <h3>Date</h3>
        <DatePicker
          selected={date}
          onChange={(date) => setDate(date)}
          minDate={new Date()}
          className="DatePicker"
        />
      </section>
      {!isPoll && (
        <section className="TweetImagesContainer">
          <div className="TweetImagesHeader">
            <h3>Images</h3>
            <DeleteForeverOutlinedIcon onClick={() => setFiles(null)} />
          </div>
          <div className="DropContainer" {...getRootProps()}>
            <div>
              <input {...getInputProps()} />
              {isDragActive ? (
                <div className="DropContainerInside">
                  <CloudUploadIcon />
                  <strong>Drop your images here ...</strong>
                </div>
              ) : (
                <div className="DropContainerInside">
                  <CloudUploadIcon />
                  <strong>
                    Drag 'n' drop some images here, or click to select them
                  </strong>
                  <div>
                    {files &&
                      files.map((file) => (
                        <div key={file.name}>{file.name}</div>
                      ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      )}
      {isPoll && (
        <section className="TweetPollContainer">
          <h3>Poll options</h3>
          <TextField
            label="Option 1"
            value={pollOption1}
            onChange={(event) => setPollOption1(event.target.value)}
          />
          <TextField
            label="Option 2"
            value={pollOption2}
            onChange={(event) => setPollOption2(event.target.value)}
          />
          <TextField
            label="Option 3"
            value={pollOption3}
            onChange={(event) => setPollOption3(event.target.value)}
          />
          <TextField
            label="Option 4"
            value={pollOption4}
            onChange={(event) => setPollOption4(event.target.value)}
          />
          <TextField
            label="Poll duration (minutes)"
            type="number"
            value={pollDuration}
            onChange={(event) => setPollDuration(event.target.value)}
          />
        </section>
      )}
      <div className="ButtonContainer">
        <Button variant="contained" endIcon={<SendIcon />} onClick={submit}>
          Schedule
        </Button>
      </div>
    </div>
  );
}

export default ScheduleTweet;
