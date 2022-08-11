export const fetchAllPizzaEvents = async () => {
  const res = await fetch(`http://localhost:8080`);
  return res.json();
}
