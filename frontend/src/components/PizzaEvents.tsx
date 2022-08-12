import { useQuery } from '@tanstack/react-query'
import { IPizzaEvent, PizzaEventProps } from 'types';

function PizzaEvents({ queryKey, query } : PizzaEventProps) {
  const { isLoading, error, data } = useQuery(
      queryKey,
      query
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
            data.map((pizzaEvent : IPizzaEvent) => {
                return <PizzaEvent 
                    time={pizzaEvent.time} 
                    place={pizzaEvent.place} 
                    attendees={pizzaEvent.attendees} 
                />
            })
        }
    </>
  )
}

function PizzaEvent({time, place, attendees }: IPizzaEvent) {
    return (
        <>
            <p><b>{place}</b> - {time}</p>
            <ul>
                {attendees.map(attendee => {
                    return <li>{attendee}</li>
                })}
            </ul>
        </>
    )
}

export default PizzaEvents;