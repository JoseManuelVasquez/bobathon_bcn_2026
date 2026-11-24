package com.workshop.assetdesk.service;

import com.workshop.assetdesk.domain.SharedResource;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

public class ResourceService {
    private final Map<Long, SharedResource> resources = new LinkedHashMap<Long, SharedResource>();

    public ResourceService() {
        resources.put(1L, new SharedResource(1L, "Portátil de formación", "COMPUTING", "AVAILABLE", null));
        resources.put(2L, new SharedResource(2L, "Proyector portátil", "PRESENTATION", "ASSIGNED", "Equipo Beta"));
        resources.put(3L, new SharedResource(3L, "Kit de pruebas", "TESTING", "AVAILABLE", null));
        resources.put(4L, new SharedResource(4L, "Equipo de videoconferencia", "COMMUNICATION", "AVAILABLE", null));
    }

    public synchronized List<SharedResource> findAll() {
        List<SharedResource> result = new ArrayList<SharedResource>();
        for (SharedResource resource : resources.values()) { result.add(resource.copy()); }
        return result;
    }

    public synchronized SharedResource findById(long id) { return require(id).copy(); }

    public synchronized SharedResource assign(long id, String team) {
        if (team == null || team.trim().isEmpty() || team.trim().length() > 120) {
            throw new IllegalArgumentException("El equipo es obligatorio y admite hasta 120 caracteres.");
        }
        SharedResource resource = require(id);
        if (!"AVAILABLE".equals(resource.getStatus())) {
            throw new IllegalStateException("El recurso ya está asignado.");
        }
        resource.assign(team.trim());
        return resource.copy();
    }

    public synchronized SharedResource release(long id) {
        SharedResource resource = require(id);
        if (!"ASSIGNED".equals(resource.getStatus())) {
            throw new IllegalStateException("El recurso no está asignado.");
        }
        resource.release();
        return resource.copy();
    }

    public synchronized Map<String, Integer> summary() {
        int available = 0;
        for (SharedResource resource : resources.values()) {
            if ("AVAILABLE".equals(resource.getStatus())) { available++; }
        }
        Map<String, Integer> result = new LinkedHashMap<String, Integer>();
        result.put("total", resources.size());
        result.put("available", available);
        result.put("assigned", resources.size() - available);
        return result;
    }

    private SharedResource require(long id) {
        SharedResource resource = resources.get(id);
        if (resource == null) { throw new NoSuchElementException("Recurso no encontrado."); }
        return resource;
    }
}
