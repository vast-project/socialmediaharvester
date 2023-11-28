import { useEffect, useState } from "react";
import SocialCard from "../components/SocialCard";
import "./TweetList.css";
import { ApiConnector } from "../api/ApiConnector";
import { useNavigate } from "react-router-dom";

function TweetList() {
  const navigate = useNavigate();
  const { getPosts } = ApiConnector();
  const [posts, setPosts] = useState(null);

  useEffect(() => {
    async function fetchPosts() {
      const posts = await getPosts();
      setPosts(posts);
    }
    fetchPosts();
  }, []);

  return (
    <div className="TweetList">
      <h2>TWEETS LIST</h2>
      <div className="SocialCardsContainer">
        {posts &&
          posts.map((post) => (
            <SocialCard
              key={post.post_id}
              id={post.post_id}
              date={post.due}
              status={post.status}
              responses={post.responses}
              text={post.text}
              onClick={() => navigate(`/tweet/${post.post_id}`)}
            />
          ))}
      </div>
    </div>
  );
}

export default TweetList;
