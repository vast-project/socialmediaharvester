import "./CommentCard.css";

function CommentCard({ author, comment }) {
  return (
    <div className="CommentCard">
      <div className="Author">
        <strong>Author: </strong>
        {author}
      </div>
      <div className="Comment">{comment}</div>
    </div>
  );
}

export default CommentCard;
