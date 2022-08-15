import { useQuery } from '@tanstack/react-query'
import { IPizzaEvent, PizzaEventProps } from 'types';
import { Typography } from '@mui/material';
import { type } from 'os';
import { datePickerValueManager } from '@mui/x-date-pickers/DatePicker/shared';

function PizzaEvents({ queryKey, query } : PizzaEventProps) {
  const { isLoading, error, data } = useQuery(
      queryKey,
      query
  )

  if (isLoading) return (
      <Typography variant="subtitle1">Loading...</Typography>
  )
      
  if (error) return (
    <Typography variant="subtitle1">Could not fetch pizza events</Typography>
    )

  if (data === undefined || data.length == 0) {
      return (
          <Typography variant="subtitle1">No pizza events :(</Typography>
      )
  }

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
    function convertToDateObject(timestring: string){
        //Wed, 19 Oct 2016 18:00:00 GMT
        const strings = timestring.split(' ').slice(1, 5)
        const month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        const clockstrings = strings[3].split(":")
        return new Date(parseInt(strings[2]), month.indexOf(strings[1]), parseInt(strings[0]), parseInt(clockstrings[0]), parseInt(clockstrings[1]), parseInt(clockstrings[2]))
    }
    const date = convertToDateObject(time)
    const dayOfTheWeek = date.toLocaleDateString('en-US', {weekday: 'short'})
    let datestring =  date.toLocaleDateString('no-NO')
    let [day, month, year] = datestring.split(".")  
    let minutes = date.getMinutes().toString()
    minutes = minutes.length == 1 ? "0" + minutes : minutes
    day = day.length == 1 ? "0" + day : day
    month = month.length == 1 ? "0" + month : month
    
    
    return (
        <>
            <h3>{dayOfTheWeek} {day}.{month}.{year}</h3>
            <p><b>{date.getHours()}:{minutes}</b></p>
            <p><b>{place}</b></p>
            <ul>
                {attendees.map(attendee => {
                    return <li>{attendee}</li>
                })}
            </ul>
        </>
    )
}

export default PizzaEvents;