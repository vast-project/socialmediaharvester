import { atom } from "recoil";

export const authTokenAtom = atom({
  key: "authTokenState",
  default: null,
});
