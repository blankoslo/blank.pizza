const BASE_URL = 'https://reqres.in'

export const fetchAllPizzaEvents = async () => {
  const res = await fetch(BASE_URL + `/api/users?page=2`);
  return res.json();
}
