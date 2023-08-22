import axios from "axios";
import config from '../config.json';


export const getPropertyNeighbords = (id, distance = 70000) => {
  return axios.get(`${config.API_HOST}/neighbords/${id}?distance_m=${distance}`)
}