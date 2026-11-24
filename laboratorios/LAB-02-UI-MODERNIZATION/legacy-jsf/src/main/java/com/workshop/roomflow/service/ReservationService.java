package com.workshop.roomflow.service;

import com.workshop.roomflow.domain.Reservation;
import java.time.LocalDate;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.NoSuchElementException;

public class ReservationService {
    private static final ReservationService INSTANCE = new ReservationService();
    private final Map<Long, Reservation> reservations = new LinkedHashMap<Long, Reservation>();
    private final Map<String, Integer> rooms = new LinkedHashMap<String, Integer>();
    private long nextId = 5L;

    public ReservationService() {
        rooms.put("Atlas", 12); rooms.put("Norte", 8); rooms.put("Taller", 20);
        reservations.put(1L, new Reservation(1L, "Ana Torres", "Atlas", "2027-04-12", "MORNING", 6, "REQUESTED"));
        reservations.put(2L, new Reservation(2L, "Luis Moreno", "Norte", "2027-04-12", "AFTERNOON", 4, "CONFIRMED"));
        reservations.put(3L, new Reservation(3L, "Marta Vidal", "Taller", "2027-04-13", "MORNING", 12, "REQUESTED"));
        reservations.put(4L, new Reservation(4L, "Diego Ríos", "Atlas", "2027-04-13", "AFTERNOON", 5, "CANCELLED"));
    }

    public static ReservationService getInstance() { return INSTANCE; }
    public List<String> roomNames() { return new ArrayList<String>(rooms.keySet()); }

    public synchronized List<Reservation> findAll(String search) {
        String term = search == null ? "" : search.trim().toLowerCase(Locale.ROOT);
        List<Reservation> result = new ArrayList<Reservation>();
        for (Reservation reservation : reservations.values()) {
            if ((reservation.getOrganizer() + " " + reservation.getRoom()).toLowerCase(Locale.ROOT).contains(term)) {
                result.add(reservation.copy());
            }
        }
        return result;
    }
    public synchronized Reservation findById(long id) { return require(id).copy(); }

    public synchronized Reservation create(String organizer, String room, String date, String slot, int attendees) {
        if (organizer == null || organizer.trim().isEmpty() || organizer.trim().length() > 120) {
            throw new IllegalArgumentException("Organizador obligatorio, hasta 120 caracteres.");
        }
        if (!rooms.containsKey(room)) { throw new IllegalArgumentException("Sala desconocida."); }
        try { LocalDate.parse(date == null ? "" : date); }
        catch (DateTimeParseException ex) { throw new IllegalArgumentException("Fecha inválida; utiliza AAAA-MM-DD."); }
        if (!"MORNING".equals(slot) && !"AFTERNOON".equals(slot)) {
            throw new IllegalArgumentException("Selecciona mañana o tarde.");
        }
        if (attendees < 1 || attendees > rooms.get(room)) {
            throw new IllegalArgumentException("El número de asistentes supera el aforo o es menor que uno.");
        }
        Reservation created = new Reservation(nextId++, organizer.trim(), room, date, slot, attendees, "REQUESTED");
        reservations.put(created.getId(), created);
        return created.copy();
    }

    public synchronized Reservation confirm(long id) {
        Reservation selected = require(id);
        if (!"REQUESTED".equals(selected.getStatus())) { throw new IllegalStateException("Solo se confirman solicitudes pendientes."); }
        for (Reservation other : reservations.values()) {
            if (other.getId() != id && "CONFIRMED".equals(other.getStatus())
                    && other.getRoom().equals(selected.getRoom()) && other.getDate().equals(selected.getDate())
                    && other.getSlot().equals(selected.getSlot())) {
                throw new IllegalStateException("La sala ya está ocupada en esa fecha y franja.");
            }
        }
        selected.setStatus("CONFIRMED");
        return selected.copy();
    }

    public synchronized Reservation cancel(long id) {
        Reservation selected = require(id);
        if ("CANCELLED".equals(selected.getStatus())) { throw new IllegalStateException("La reserva ya está cancelada."); }
        selected.setStatus("CANCELLED");
        return selected.copy();
    }

    private Reservation require(long id) {
        Reservation selected = reservations.get(id);
        if (selected == null) { throw new NoSuchElementException("Reserva no encontrada."); }
        return selected;
    }
}
