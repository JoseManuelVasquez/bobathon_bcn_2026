<%@ page contentType="text/html; charset=UTF-8" %><%@ taglib prefix="s" uri="/struts-tags" %>
<!doctype html><html lang="es"><head><meta charset="utf-8"><title>RoomFlow - Detalle</title><link rel="stylesheet" href="legacy.css"></head><body>
<div class="header">ROOMFLOW | Detalle de reserva | Struts</div><a href="reservations.action">Volver al listado</a><s:actionerror/><s:actionmessage/>
<h1>Reserva #<s:property value="selected.id"/></h1><p>Organizador: <s:property value="selected.organizer"/></p>
<p>Sala: <s:property value="selected.room"/></p><p>Fecha: <s:property value="selected.date"/></p>
<p>Franja: <s:property value="selected.slot"/></p><p>Asistentes: <s:property value="selected.attendees"/></p>
<p>Estado: <strong><s:property value="selected.status"/></strong></p>
<s:if test="selected.status == 'REQUESTED'"><s:form action="confirm" method="post"><s:hidden name="id"/><s:submit value="Confirmar"/></s:form></s:if>
<s:if test="selected.status != 'CANCELLED'"><s:form action="cancel" method="post"><s:hidden name="id"/><s:submit value="Cancelar reserva"/></s:form></s:if>
</body></html>
