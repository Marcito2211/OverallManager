import datetime
import os.path
import streamlit as st
from dateutil import parser 

from dataclasses import dataclass

def check_hour()

def make_day(day_schedule):
  
  for hour in range(24):
    col_time, col_event = st.columns([1, 6])
    time_str = f"{hour:02d}:00"
    col_time.markdown(f"<div style='padding:10px 0;'><strong>{time_str}</strong></div>", unsafe_allow_html=True)

    event = day_schedule.get(hour)
    if event:
        # for event in day_schedule[hour]:
          col_event.markdown(
              f"<div style='background-color:#d0f0c0; padding:10px; border-radius:8px;'>{event.summary}<br><small>{even('%H:%M')} – {event.end.strftime('%H:%M')}</small></div>",
              unsafe_allow_html=True
          )
    else:
        col_event.markdown(
            "<div style='border:1px dashed #ccc; padding:10px; border-radius:8px; color:#aaa;'>Free</div>",
            unsafe_allow_html=True
        )
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