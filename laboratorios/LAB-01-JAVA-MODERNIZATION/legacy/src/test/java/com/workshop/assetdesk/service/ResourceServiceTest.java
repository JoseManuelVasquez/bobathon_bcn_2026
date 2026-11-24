package com.workshop.assetdesk.service;

import org.junit.Test;
import static org.junit.Assert.*;

public class ResourceServiceTest {
    @Test public void seedHasFourResourcesAndThreeAvailable() {
        ResourceService service = new ResourceService();
        assertEquals(Integer.valueOf(4), service.summary().get("total"));
        assertEquals(Integer.valueOf(3), service.summary().get("available"));
    }

    @Test public void assignmentAndReleaseRestoreAvailability() {
        ResourceService service = new ResourceService();
        assertEquals("ASSIGNED", service.assign(1, "Equipo Demo").getStatus());
        assertEquals(Integer.valueOf(2), service.summary().get("available"));
        assertEquals("AVAILABLE", service.release(1).getStatus());
        assertEquals(Integer.valueOf(3), service.summary().get("available"));
    }

    @Test(expected = IllegalStateException.class) public void assignedResourceCannotBeAssignedAgain() {
        new ResourceService().assign(2, "Otro equipo");
    }
}
