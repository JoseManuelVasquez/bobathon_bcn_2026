package com.workshop.assetdesk;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.workshop.assetdesk.service.ResourceService;
import java.io.PrintStream;
import java.util.LinkedHashMap;
import java.util.Map;

public class AssetDeskApplication {
    public static void main(String[] args) {
        int exitCode = run(args, System.out, System.err);
        if (exitCode != 0) {
            System.exit(exitCode);
        }
    }

    static int run(String[] args, PrintStream out, PrintStream err) {
        String command = args.length == 0 ? "list" : args[0];
        if (!"list".equals(command) && !"demo".equals(command)) {
            err.println("Uso: java -jar target/assetdesk.jar [list|demo]");
            return 2;
        }
        ResourceService service = new ResourceService();
        Map<String, Object> output = new LinkedHashMap<String, Object>();
        output.put("application", "AssetDesk");
        output.put("initialSummary", service.summary());
        if ("demo".equals(command)) {
            output.put("assignment", service.assign(1L, "Equipo Demo"));
            output.put("afterAssignment", service.summary());
            output.put("release", service.release(1L));
            output.put("afterRelease", service.summary());
        }
        output.put("resources", service.findAll());
        Gson gson = new GsonBuilder().serializeNulls().setDateFormat("yyyy-MM-dd").setPrettyPrinting().create();
        out.println(gson.toJson(output));
        return 0;
    }
}
