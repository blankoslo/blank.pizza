import { useQuery } from '@tanstack/react-query'

import { fetchAllPizzaEvents } from 'queries';
import { IPizzaEvent } from 'types';

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