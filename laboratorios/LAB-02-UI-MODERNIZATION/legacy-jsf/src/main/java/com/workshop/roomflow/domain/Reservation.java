package com.workshop.roomflow.domain;

import java.io.Serializable;

public class Reservation implements Serializable {
    private static final long serialVersionUID = 1L;
    private final long id;
    private final String organizer;
    private final String room;
    private final String date;
    private final String slot;
    private final int attendees;
    private String status;

    public Reservation(long id, String organizer, String room, String date, String slot, int attendees, String status) {
        this.id = id; this.organizer = organizer; this.room = room; this.date = date;
        this.slot = slot; this.attendees = attendees; this.status = status;
    }
    public Reservation copy() { return new Reservation(id, organizer, room, date, slot, attendees, status); }
    public long getId() { return id; }
    public String getOrganizer() { return organizer; }
    public String getRoom() { return room; }
    public String getDate() { return date; }
    public String getSlot() { return slot; }
    public int getAttendees() { return attendees; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
