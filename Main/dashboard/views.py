# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required


# @login_required
# def dashboard_view(request):

#     user = request.user

#     if user.role == 'admin':
#         return render(request, 'dashboard/admin_dashboard.html')

#     elif user.role == 'manager':
#         return render(request, 'dashboard/manager_dashboard.html')

#     elif user.role == 'associate':
#         return render(request, 'dashboard/associate_dashboard.html')

#     elif user.role == 'client':
#         return render(request, 'dashboard/client_dashboard.html')

#     return redirect('login')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from projects.models import Project
import json


@login_required
def dashboard_view(request):

    user = request.user

    # if user.role == "admin":

    #     total_projects = Project.objects.count()
    #     total_clients = Project.objects.values("client").distinct().count()
    #     total_revenue = Project.objects.aggregate(
    #         total=Sum("price_bid")
    #     )["total"] or 0

    #     recent_projects = Project.objects.order_by("-created_at")[:5]

    #     return render(request, "dashboard/admin_dashboard.html", {
    #         "total_projects": total_projects,
    #         "total_clients": total_clients,
    #         "total_revenue": total_revenue,
    #         "recent_projects": recent_projects,
    #     })

    if user.role == "admin":

        total_projects = Project.objects.count()
        total_clients = Project.objects.values("client").distinct().count()
        total_revenue = Project.objects.aggregate(
            total=Sum("price_bid")
        )["total"] or 0

        recent_projects = Project.objects.order_by("-created_at")[:5]

        # ✅ Status distribution
        status_data = (
            Project.objects
            .values("status")
            .annotate(count=Count("status"))
    )

        labels = [item["status"] for item in status_data]
        counts = [item["count"] for item in status_data]

        # labels = json.dumps([item["status"] for item in status_data])
        # counts = json.dumps([item["count"] for item in status_data])

        return render(request, "dashboard/admin_dashboard.html", {
            "total_projects": total_projects,
            "total_clients": total_clients,
            "total_revenue": total_revenue,
            "recent_projects": recent_projects,
            "status_labels": labels,
            "status_counts": counts,
        })

    elif user.role == "manager":

        assigned_projects = Project.objects.filter(manager=user)
        in_progress = assigned_projects.filter(status="in_progress").count()
        completed = assigned_projects.filter(status="completed").count()

        return render(request, "dashboard/manager_dashboard.html", {
            "total_assigned": assigned_projects.count(),
            "in_progress": in_progress,
            "completed": completed,
            "recent_projects": assigned_projects.order_by("-created_at")[:5],
        })

    elif user.role == "associate":

        assigned_projects = Project.objects.filter(associates=request.user)
       

        return render(request, "dashboard/associate_dashboard.html", {
            "total_assigned": assigned_projects.count(),
            "in_progress": assigned_projects.filter(status="in_progress").count(),
            "completed": assigned_projects.filter(status="completed").count(),
            "assigned_projects": assigned_projects.order_by("-created_at")[:5],
        })

    elif user.role == "client":

        projects = Project.objects.filter(client=request.user)
        completed = projects.filter(status="completed").count()

        return render(request, "dashboard/client_dashboard.html", {
            "total_projects": projects.count(),
            "completed_projects": projects.filter(status="completed").count(),
            "recent_projects": projects.order_by("-created_at")[:5],
        })