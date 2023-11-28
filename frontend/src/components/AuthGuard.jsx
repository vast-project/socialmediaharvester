import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useRecoilValue } from "recoil";
import { authTokenAtom } from "../store/atoms/authAtom";

function AuthGuard({ children }) {
  const navigate = useNavigate();
  const authToken = useRecoilValue(authTokenAtom);

  useEffect(() => {
    if (!authToken) navigate("/login");
    if (authToken) navigate("/");
  }, []);

  if (authToken) return children;
}

export default AuthGuard;
