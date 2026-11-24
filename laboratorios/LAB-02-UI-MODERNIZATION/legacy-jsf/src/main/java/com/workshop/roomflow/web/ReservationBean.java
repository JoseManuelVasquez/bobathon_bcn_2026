package com.workshop.roomflow.web;

import com.workshop.roomflow.domain.Reservation;
import com.workshop.roomflow.service.ReservationService;
import java.io.Serializable;
import java.util.List;
import javax.faces.application.FacesMessage;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;
import javax.faces.context.FacesContext;

@ManagedBean(name = "reservations")
@SessionScoped
public class ReservationBean implements Serializable {
    private static final long serialVersionUID = 1L;
    private String search = "";
    private String organizer;
    private String room = "Atlas";
    private String date = "2027-04-14";
    private String slot = "MORNING";
    private int attendees = 1;
    private Long selectedId;

    private ReservationService service() { return ReservationService.getInstance(); }
    public List<Reservation> getItems() { return service().findAll(search); }
    public List<String> getRoomNames() { return service().roomNames(); }
    public Reservation getSelected() { return selectedId == null ? null : service().findById(selectedId); }
    public String open(long id) { selectedId = id; return "detail?faces-redirect=true"; }
    public String create() {
        try { service().create(organizer, room, date, slot, attendees); organizer = null; message("Solicitud creada."); }
        catch (IllegalArgumentException ex) { message(ex.getMessage()); }
        return null;
    }
    public String confirm() {
        try { service().confirm(selectedId); message("Reserva confirmada."); }
        catch (IllegalStateException ex) { message(ex.getMessage()); }
        return null;
    }
    public String cancel() {
        try { service().cancel(selectedId); message("Reserva cancelada."); }
        catch (IllegalStateException ex) { message(ex.getMessage()); }
        return null;
    }
    private void message(String text) { FacesContext.getCurrentInstance().addMessage(null, new FacesMessage(text)); }
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
