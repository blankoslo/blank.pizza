export const fetchAllPizzaEvents = async () => {
  const res = await fetch(`http://localhost:8080/api/events`);
  return res.json();
}

export const fetchUpcomingPizzaEvents = async () => {
  const res = await fetch(`http://localhost:8080/api/future_events`);
  return res.json();
}
