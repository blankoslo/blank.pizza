export interface IPizzaEvent {
    time: string,
    place: string,
    attendees: string[],
}

export interface PizzaEventProps {
    queryKey: string[],
    query: () => Promise<any>,
}