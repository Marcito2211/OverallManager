import datetime
import os.path
import streamlit as st
from dateutil import parser 

from dataclasses import dataclass
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]



import streamlit as st

st.markdown("""
<style>
.left-col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    max-height: 1200px;
}
  .right-col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    max-height: 1200px;
}
.hour-label {
    height: 50px;
    line-height: 50px;
    border-top: 1px solid #eee;
    font-weight: bold;
}
.event-block {
    background-color: #d0ebff;
    border-radius: 8px;
    cursor: pointer;
}
.event-block:hover{
     filter: brightness(95%);
}
.empty-block {
    height: 50px;
    border-top: 1px solid #eee;
}
.clickable-empty {
    cursor: pointer;
}
.clickable-empty :hover {
    background-color:#f0eded;
}
</style>
""", unsafe_allow_html=True)


def  make_day(day_schedule):
  hours = list(range(5,24))
  col1, col2 = st.columns([1, 5])
  buffer = 0
  empty_section = ""

  with col1:
      st.markdown('<div class="left-col">', unsafe_allow_html=True)
      for hour in hours:
          st.markdown(f'<div class="hour-label">{hour:02d}:00</div>', unsafe_allow_html=True)
      st.markdown('</div>', unsafe_allow_html=True)

  with col2:
      st.markdown('<div class="right-col">', unsafe_allow_html=True)
      ##st.markdown('<div style = "height:25px;"></div>', unsafe_allow_html=True)
      for hour in hours:
          event = day_schedule.get(hour)
          if event:
              
              if empty_section:
                    st.markdown(
                        f'<div class="clickable-empty">{empty_section}</div>',
                        unsafe_allow_html=True
                    )
                    empty_section = ""

              st.markdown(
                  f'<div class="event-block" style="height:{event.duration*5/6}px;">{event.summary}<br><small>{event.start.strftime("%H:%M")} - {event.end.strftime("%H:%M")}</small></div>',
                  unsafe_allow_html=True)
              if event.duration > 60:
                 buffer += event.duration%60
          else:
              if buffer > 0:
                 empty_section += f'<div style="height:{buffer*5/6}px;"></div>'
                 #st.markdown(f'<div style="height:{buffer*5/6}px;"></div>', unsafe_allow_html=True)
                 amount_to_subtract = min(buffer, 60)
                 buffer -= amount_to_subtract
              else: 
                 empty_section += '<div class="empty-block">&nbsp;</div>'
      if empty_section:
                  st.markdown(
                      f'<div class="clickable-empty">{empty_section}</div>',
                      unsafe_allow_html=True
                  )
                  empty_section = ""

      
              
              
      st.markdown('</div>', unsafe_allow_html=True)

  # for hour in range(5,24):
  #   col_time,col_event = st.columns([1,5])
  #   time_str = f"{hour:02d}:00"
  #   col_time.markdown(f"<div style='padding:10px 0;'><strong>{time_str}</strong></div>", unsafe_allow_html=True)
  #   event = day_schedule.get(hour, [])
    # if event:
    #   col2.success(f"{event.summary} ({event.start.strftime('%H:%M')}–{event.end.strftime('%H:%M')})")
        # for event in events:
        #     col2.success(f"{event.summary} ({event.start.strftime('%H:%M')}–{event.end.strftime('%H:%M')})")
    # else:
    #     col2.markdown("&nbsp;", unsafe_allow_html=True)  # Empty space


@dataclass
class CalendarEvent:
  summary : str
  start: datetime.datetime
  end: datetime.datetime
  duration: datetime.timedelta
    

def event_to_data(event_dict):
  All_Events = {}
  for event in event_dict:
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    start_formatted = parser.isoparse(start)
    end_formatted = parser.isoparse(end)
    duration = end_formatted-start_formatted
    minutes = duration.total_seconds()/60
    event_object = CalendarEvent(summary=event.get("summary", "No Title"),start=start_formatted,end=end_formatted,duration=minutes)
    
    All_Events[start_formatted.hour] = event_object
  return(All_Events)

    
  
  # for event in event_dict:

  
  
  
def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    today = datetime.date.today()
    print("Getting the upcoming 10 events")
    timeStart = str(today) +"T00:00:00Z"
    timeEnd = str(today) +"T23:59:59Z"
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=timeStart,
            timeMax = timeEnd,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
            timeZone='Europe/Ireland'
        )
        .execute()
    )
    events = events_result.get("items", [])
    #test = CalendarEvent(summary="hi",start =1,end =2)
    formatted_events = event_to_data(events)
    make_day(formatted_events)

    if not events:
      print("No upcoming events found.")
      return
    

    # Prints the start and name of the next 10 events
    for event in events:
      #print(event)
      start = event["start"].get("dateTime", event["start"].get("date"))
      #print(start, event["summary"])

  

  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  main()