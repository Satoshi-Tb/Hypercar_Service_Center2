from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render
from collections import deque
from django.http import HttpResponse
from django.http import HttpResponseRedirect

class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "menu/index.html", context={"menu_list": menu_list2})


class TicketView(View):
    def get(self, request, service, *args, **kwargs):
        global ticket_seq
        ticket_seq += 1
        if service == "change_oil":
            item = ChangeOilService(ticket_seq)
        elif service == "inflate_tires":
            item = InflateTiresService(ticket_seq)
        elif service == "diagnostic":
            item = DiagnosticsService(ticket_seq)
        else:
            None  # TODO?

        service_list.append(item)
        context = {
            "ticket_number": item.ticket_number,
            "minutes_to_wait": service_list.minutes_to_wait(item.ticket_number),
            "queue_length": service_list.size()
        }
        return render(request, "ticket/index.html", context=context)


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "change_oil_count": service_list.change_oil_count(),
            "inflate_tires_count": service_list.inflate_tires_count(),
            "diagnostic_count": service_list.diagnostic_count(),
        }
        return render(request, "processing/index.html", context=context)

    def post(self, request, *args, **kwargs):
        global processing_service
        if service_list.size() > 0:
            processing_service = service_list.pop()
        else:
            processing_service = None

        return HttpResponseRedirect("next")


class NextView(View):
    def get(self, request, *args, **kwargs):
        global processing_service
        context = {
            "next": processing_service
        }
        return render(request, "processing/next.html", context=context)


class Service:
    def __init__(self, name, minutes_taken, description, prior, ticket_number):
        self.name = name
        self.minutes_taken = minutes_taken
        self.description = description
        self.prior = prior
        self.ticket_number = ticket_number


class ChangeOilService(Service):
    def __init__(self, ticket_number):
        super().__init__("change_oil", 2, "Change oil", 1, ticket_number)


class InflateTiresService(Service):
    def __init__(self, ticket_number):
        super().__init__("inflate_tires", 5, "Inflate tires", 2, ticket_number)


class DiagnosticsService(Service):
    def __init__(self, ticket_number):
        super().__init__("diagnostic", 30, "Get diagnostic test", 3, ticket_number)


class ServiceQueue:
    def __init__(self):
        self.service_queue = deque()

    def top(self):
        return self.service_queue[0] if len(self.service_queue) > 0 else None

    def append(self, service: Service):
        for i, s in enumerate(self.service_queue):
            if service.prior < s.prior:
                self.service_queue.insert(i, service)
                return
        # 最後に追加
        self.service_queue.append(service)

    def pop(self):
        return self.service_queue.popleft()

    def minutes_to_wait(self, ticket_no):
        minutes = 0
        for i, s in enumerate(self.service_queue):
            if ticket_no == s.ticket_number:
                break
            minutes += s.minutes_taken
        return minutes

    def size(self):
        return len(self.service_queue)

    def change_oil_count(self):
        return len([s for s in self.service_queue if s.name == "change_oil"])

    def inflate_tires_count(self):
        return len([s for s in self.service_queue if s.name == "inflate_tires"])

    def diagnostic_count(self):
        return len([s for s in self.service_queue if s.name == "diagnostic"])


# session or application scope
service_list = ServiceQueue()
processing_service = None
ticket_seq = 0
menu_list2 = [
    ChangeOilService(0),
    InflateTiresService(0),
    DiagnosticsService(0)
]