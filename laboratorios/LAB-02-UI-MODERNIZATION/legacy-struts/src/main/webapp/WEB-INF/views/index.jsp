<%@ page contentType="text/html; charset=UTF-8" %><%@ taglib prefix="s" uri="/struts-tags" %>
<!doctype html><html lang="es"><head><meta charset="utf-8"><title>RoomFlow - Reservas</title><link rel="stylesheet" href="legacy.css"></head><body>
<div class="header">ROOMFLOW | Reserva de salas | Struts</div><h1>Reservas de espacios</h1>
<p>Atlas: 12 plazas · Norte: 8 plazas · Taller: 20 plazas</p><s:actionerror/><s:actionmessage/>
<s:form action="reservations" method="get"><s:textfield name="search" label="Sala u organizador"/><s:submit value="Buscar"/></s:form>
<table border="1" cellpadding="8"><thead><tr><th>ID</th><th>Organizador</th><th>Sala</th><th>Fecha</th><th>Franja</th><th>Estado</th><th>Detalle</th></tr></thead><tbody>
<s:iterator value="reservations"><tr>
<td><s:property value="id"/></td><td><s:property value="organizer"/></td><td><s:property value="room"/></td>
<td><s:property value="date"/></td><td><s:property value="slot"/></td><td><s:property value="status"/></td>
<td><s:url var="detailUrl" action="detail"><s:param name="id" value="id"/></s:url><a href="<s:property value='#detailUrl'/>">Abrir</a></td>
</tr></s:iterator></tbody></table>
<h2>Nueva reserva</h2><s:form action="create" method="post">
<s:textfield name="organizer" label="Organizador" maxlength="120"/>
<s:select name="room" label="Sala" list="roomNames"/>
<s:textfield name="date" label="Fecha AAAA-MM-DD"/>
<s:select name="slot" label="Franja" list="#{'MORNING':'Mañana','AFTERNOON':'Tarde'}"/>
<s:textfield name="attendees" label="Asistentes"/><s:submit value="Crear reserva"/>
</s:form></body></html>
