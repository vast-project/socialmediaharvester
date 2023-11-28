import "./SocialCard.css";
import { Paper } from "@mui/material";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";

function SocialCard({ id, date, status, responses, text, onClick }) {
  return (
    <Paper elevation={0} className="SocialCard" onClick={onClick}>
      <div className="SocialHead">
        <span>
          <strong>ID :</strong> {id}
        </span>
        <span>
          <strong>Date: </strong> {date}
        </span>
        <span>
          <strong>Status: </strong> {status}
        </span>
        <span>
          {responses}{" "}
          <ChatBubbleOutlineIcon
            style={{ width: 20 }}
            className="ResponsesIcon"
          />
        </span>
      </div>
      <div className="SocialText">{text}</div>
    </Paper>
  );
}

export default SocialCard;
