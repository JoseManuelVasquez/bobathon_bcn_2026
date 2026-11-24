package com.workshop.roomflow.web;

import com.opensymphony.xwork2.ActionSupport;
import com.workshop.roomflow.domain.Reservation;
import com.workshop.roomflow.service.ReservationService;
import java.util.List;

public class ReservationAction extends ActionSupport {
    private static final long serialVersionUID = 1L;
    private Long id;
    private String search;
    private String organizer;
    private String room = "Atlas";
    private String date = "2027-04-14";
    private String slot = "MORNING";
    private int attendees = 1;

    private ReservationService service() { return ReservationService.getInstance(); }
    public String execute() { return SUCCESS; }
    public String detail() {
        try { service().findById(id == null ? -1 : id); return SUCCESS; }
        catch (RuntimeException ex) { addActionError(ex.getMessage()); return ERROR; }
    }
    public String create() {
        try { service().create(organizer, room, date, slot, attendees); addActionMessage("Solicitud creada."); return SUCCESS; }
        catch (IllegalArgumentException ex) { addActionError(ex.getMessage()); return ERROR; }
    }
    public String confirm() {
        try { service().confirm(id == null ? -1 : id); addActionMessage("Reserva confirmada."); return SUCCESS; }
        catch (RuntimeException ex) { addActionError(ex.getMessage()); return ERROR; }
    }
    public String cancel() {
        try { service().cancel(id == null ? -1 : id); addActionMessage("Reserva cancelada."); return SUCCESS; }
        catch (RuntimeException ex) { addActionError(ex.getMessage()); return ERROR; }
    }
    public List<Reservation> getReservations() { return service().findAll(search); }
    public List<String> getRoomNames() { return service().roomNames(); }
    public Reservation getSelected() { return id == null ? null : service().findById(id); }
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getSearch() { return search; }
    public void setSearch(String search) { this.search = search; }
    public String getOrganizer() { return organizer; }
    public void setOrganizer(String organizer) { this.organizer = organizer; }
    public String getRoom() { return room; }
    public void setRoom(String room) { this.room = room; }
    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }
    public String getSlot() { return slot; }
    public void setSlot(String slot) { this.slot = slot; }
    public int getAttendees() { return attendees; }
    public void setAttendees(int attendees) { this.attendees = attendees; }
}
