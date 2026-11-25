package com.workshop.assetdesk;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.apache.commons.lang3.StringUtils;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;

public class AssetDeskApplicationTest {
    @Test
    public void defaultCommandPrintsInventoryAsJson() throws Exception {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        ByteArrayOutputStream errors = new ByteArrayOutputStream();
        try (PrintStream out = new PrintStream(output, true, StandardCharsets.UTF_8.name());
             PrintStream err = new PrintStream(errors, true, StandardCharsets.UTF_8.name())) {
            assertEquals(0, AssetDeskApplication.run(new String[0], out, err));
        }

        JsonObject inventory = JsonParser.parseString(output.toString(StandardCharsets.UTF_8.name())).getAsJsonObject();
        assertEquals("AssetDesk", inventory.get("application").getAsString());
        assertEquals(4, inventory.getAsJsonArray("resources").size());
        assertFalse(inventory.has("assignment"));
        assertEquals(0, errors.size());
    }

    @Test
    public void unknownCommandPrintsUsageOnStandardError() throws Exception {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        ByteArrayOutputStream errors = new ByteArrayOutputStream();
        try (PrintStream out = new PrintStream(output, true, StandardCharsets.UTF_8.name());
             PrintStream err = new PrintStream(errors, true, StandardCharsets.UTF_8.name())) {
            assertEquals(2, AssetDeskApplication.run(new String[]{"unknown"}, out, err));
        }

        assertEquals(0, output.size());
        assertEquals("Uso: java -jar target/assetdesk.jar [list|demo]",
                StringUtils.normalizeSpace(errors.toString(StandardCharsets.UTF_8.name())));
    }
}
