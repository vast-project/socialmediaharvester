import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Gallery } from "react-grid-gallery";
import "./Tweet.css";
import { ApiConnector } from "../api/ApiConnector";
import CommentCard from "../components/CommentCard";
import SyncOutlinedIcon from "@mui/icons-material/SyncOutlined";
import PollChart from "../components/PollChart";

function Tweet() {
  const { id } = useParams();
  const { getPost, flush } = ApiConnector();
  const [post, setPost] = useState(null);

  useEffect(() => {
    async function fetchPost() {
      const post = await getPost(id);
      setPost(post);
    }
    fetchPost();
  }, [id]);

  return (
    <div className="Tweet">
      {post && (
        <>
          <h2>TWEET ID: {post.id}</h2>
          <p>
            <strong>Status: </strong>
            {post.status.status_name}
          </p>
          <p>
            <strong>Scheduled date: </strong>
            {post.due}
          </p>
          <section>
            <strong>Tweet text: </strong>
            <p>{post.text}</p>
          </section>
          <section className="pollContainer">
            <h3>POLL</h3>
            <PollChart />
          </section>
          <section className="imagesContainer">
            <h3>IMAGES</h3>
            <Gallery
              images={post.images.map((image) => ({
                src: image,
                width: 320,
                height: 174,
              }))}
              enableImageSelection={false}
            />
          </section>
          <section>
            <div className="CommentsHead">
              <h3>COMMENTS ({post.comments.length})</h3>
              <SyncOutlinedIcon
                className="RefreshIcon"
                onClick={() => flush()}
              />
            </div>
            <div className="CommentsContainer">
              {post.comments.map((comment) => (
                <CommentCard
                  key={comment.id}
                  author={comment.author}
                  comment={comment.comment}
                />
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

export default Tweet;
