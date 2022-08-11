import { useQuery } from '@tanstack/react-query'

import { fetchAllPizzaEvents } from 'queries';

function PizzaEvents() {
  const { isLoading, error, data } = useQuery(
      ['pizzaEvents'],
      fetchAllPizzaEvents
  )

  if (isLoading) return (
      <h2>Loading...</h2>
  )

  if (error) return (
      <h2>
          Could not fetch pizza events
      </h2>
  )

  return (
    <>
        {
            data.data.map((pizzaEvent : any) => {
                return (
                    <p key={pizzaEvent.id}>{pizzaEvent.first_name}</p>
                )
            })
        }
    </>
  )
}

export default PizzaEvents;