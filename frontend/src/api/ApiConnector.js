import { useRecoilValue } from "recoil";
import { authTokenAtom } from "../store/atoms/authAtom";

export function ApiConnector() {
  const authToken = useRecoilValue(authTokenAtom);

  console.log("authToken", authToken);

  const API_SERVER = import.meta.env.VITE_API_SERVER;
  const myHeaders = new Headers();
  myHeaders.append("accept", "application/json");
  myHeaders.append("Authorization", "Basic d2l0dGVydGVzdDU1NTU1Og==");

  const getRequestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };

  async function login() {
    const response = await fetch(
      `${API_SERVER}/identity/login`,
      getRequestOptions
    );
    const parsedData = await response.json();
    return parsedData;
  }

  async function getPosts() {
    const response = await fetch(
      `${API_SERVER}/post/?network_id=1`,
      getRequestOptions
    );
    const parsedData = await response.json();
    return parsedData.status;
  }

  async function getPost(id) {
    const response = await fetch(
      `${API_SERVER}/post/post/${id}/responses/?network_id=1`,
      getRequestOptions
    );
    const parsedData = await response.json();
    return parsedData.status;
  }

  async function postContent({ text, date, images }) {
    const myHeaders = new Headers();
    myHeaders.append("accept", "application/json");
    myHeaders.append("Content-Type", "application/json");
    myHeaders.append("Authorization", "Basic d2l0dGVydGVzdDU1NTU1Og==");

    let raw;
    if (images) {
      const imagesArray = [];
      images.forEach((image) =>
        imagesArray.push({
          path: image,
        })
      );
      raw = JSON.stringify(imagesArray);
    }

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: images ? raw : null,
      redirect: "follow",
    };

    await fetch(
      `${API_SERVER}/post/content/${text}/due/${date}?social_network_id=1`,
      requestOptions
    );
  }

  async function postPoll({ text, duration, options, date }) {
    const myHeaders = new Headers();
    myHeaders.append("accept", "application/json");
    myHeaders.append("Authorization", "Basic d2l0dGVydGVzdDU1NTU1Og==");

    const requestOptions = {
      method: "POST",
      headers: myHeaders,
      redirect: "follow",
    };

    const x = `${API_SERVER}/post/poll/content/${text}/due/${date}?${options}&duration_minute=${Number(
      duration
    )}&social_network_id=1`;

    await fetch(
      `${API_SERVER}/post/poll/content/${text}/due/${date}?${options}&duration_minute=${Number(
        duration
      )}&social_network_id=1`,
      requestOptions
    );
  }

  async function uploadImage(file) {
    const myHeaders = new Headers();
    myHeaders.append("accept", "application/json");

    const formdata = new FormData();
    formdata.append("file", file);

    const uploadImageRequestOptions = {
      method: "POST",
      headers: myHeaders,
      body: formdata,
      redirect: "follow",
    };

    const response = await fetch(
      `${API_SERVER}/media`,
      uploadImageRequestOptions
    );

    const parsedRes = await response.json();
    return parsedRes.filename;
  }

  return {
    getPosts,
    getPost,
    postContent,
    postPoll,
    uploadImage,
    login,
  };
}
