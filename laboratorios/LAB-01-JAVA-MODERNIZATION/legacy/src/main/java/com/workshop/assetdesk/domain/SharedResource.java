package com.workshop.assetdesk.domain;

import java.util.Date;

public class SharedResource {
    private final long id;
    private final String name;
    private final String category;
    private final Date registeredAt;
    private String status;
    private String assignedTo;

    public SharedResource(long id, String name, String category, String status, String assignedTo) {
        this.id = id; this.name = name; this.category = category;
        this.status = status; this.assignedTo = assignedTo;
        this.registeredAt = new Date(1609459200000L);
    }

    public SharedResource copy() { return new SharedResource(id, name, category, status, assignedTo); }
    public long getId() { return id; }
    public String getName() { return name; }
    public String getCategory() { return category; }
    public Date getRegisteredAt() { return new Date(registeredAt.getTime()); }
    public String getStatus() { return status; }
    public String getAssignedTo() { return assignedTo; }
    public void assign(String team) { status = "ASSIGNED"; assignedTo = team; }
    public void release() { status = "AVAILABLE"; assignedTo = null; }
}
