from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm, AssignmentForm


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from django.shortcuts import get_object_or_404
from .constants import SLA_FLOW


from chat.models import Message
from chat.forms import MessageForm

from django.core.paginator import Paginator

from ai_engine.services import correct_grammar
from accounts.models import ManagerProfile, AssociateProfile


from .forms import ManagerAssignAssociatesForm
from django.contrib.auth import get_user_model

User = get_user_model()




@login_required
def project_list(request):

    user = request.user

    if user.role == 'admin':
        projects = Project.objects.all()

    elif user.role == 'manager':
        projects = Project.objects.filter(manager=user)

    elif user.role == 'associate':
        projects = Project.objects.filter(associates=user)

    elif user.role == 'client':
        projects = Project.objects.filter(client=user)

    else:
        projects = []

    return render(request, 'projects/project_list.html', {'projects': projects})

# @login_required
# def project_create(request):

#     if request.user.role != 'client':
#         return redirect('dashboard')

#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.client = request.user
#             project.save()
#             return redirect('project_list')
#     else:
#         form = ProjectForm()

#     return render(request, 'projects/project_create.html', {'form': form})

@login_required
def project_create(request):

    if request.user.role not in ['client', 'admin']:
        return HttpResponseForbidden("Not allowed")

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)

            if request.user.role == 'client':
                project.client = request.user

            project.save()
            return redirect('project_list')

    else:
        form = ProjectForm()

    return render(request, 'projects/project_create.html', {'form': form})



@login_required
def assign_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.user.role != "admin":
        return redirect("dashboard")

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=project)

        if form.is_valid():
            project = form.save(commit=False)
            project.status = "assigned"
            project.save()

            # 🔥 AUTO ASSIGN LOGIC STARTS HERE

            try:
                manager_profile = ManagerProfile.objects.get(
                    user=project.manager
                )

                associate_profiles = AssociateProfile.objects.filter(
                    manager=manager_profile
                )

                associate_users = [a.user for a in associate_profiles]

                print("Associates found:", associate_users)

                project.associates.clear()  # important safety
                project.associates.set(associate_users)

                print("After saving:", project.associates.all())

            except ManagerProfile.DoesNotExist:
                print("ManagerProfile missing")

            return redirect("project_detail", pk=project.pk)

    else:
        form = AssignmentForm(instance=project)

    return render(request, "projects/assign_project.html", {
        "form": form,
        "project": project
    })


@login_required
def manager_assign_associates(request, pk):

    project = get_object_or_404(Project, pk=pk)

    if request.user.role != "manager":
        return redirect("dashboard")

    # only allow manager to assign their own projects
    if project.manager != request.user:
        return redirect("dashboard")

    # filter associates under this manager
    associate_profiles = AssociateProfile.objects.filter(
        manager__user=request.user
    )

    associate_users = [a.user for a in associate_profiles]

    if request.method == "POST":

        form = ManagerAssignAssociatesForm(request.POST, instance=project)

        form.fields["associates"].queryset = User.objects.filter(
            id__in=[u.id for u in associate_users]
        )

        if form.is_valid():
            form.save()
            return redirect("project_detail", pk=project.pk)

    else:

        form = ManagerAssignAssociatesForm(instance=project)

        form.fields["associates"].queryset = User.objects.filter(
            id__in=[u.id for u in associate_users]
        )

    return render(request, "projects/manager_assign.html", {
        "form": form,
        "project": project
    })


@login_required
def project_detail(request, pk):

    project = get_object_or_404(Project, pk=pk)
    user = request.user

    # 🔐 ROLE ACCESS CONTROL
    if user.role == 'client' and project.client != user:
        return HttpResponseForbidden("Not allowed")

    if user.role == 'manager' and project.manager != user:
        return HttpResponseForbidden("Not allowed")

    if user.role == 'associate' and user not in project.associates.all():
        return HttpResponseForbidden("Not allowed")

    # ✉ HANDLE MESSAGE SUBMISSION
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.project = project
            message.sender = user

        # Optional AI grammar correction
            use_ai = form.cleaned_data.get("use_ai")

            if use_ai:
                corrected_content = correct_grammar(message.content)
                message.content = corrected_content

            message.save()

            return redirect('project_detail', pk=pk)
    else:
        form = MessageForm()

    # 📄 PAGINATION
    messages_list = project.messages.all().order_by("-created_at")
    paginator = Paginator(messages_list, 10)  # 10 messages per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 🔁 SLA NEXT STATUS OPTIONS
    next_statuses = SLA_FLOW.get(project.status, [])

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'next_statuses': next_statuses,
        'page_obj': page_obj,
        'form': form
    })

@login_required
def update_project_status(request, pk):

    project = get_object_or_404(Project, pk=pk)
    user = request.user

    if request.method == "POST":

        new_status = request.POST.get("status")

        allowed = SLA_FLOW.get(project.status, [])

        if new_status not in allowed:
            return HttpResponseForbidden("Invalid status transition")

        # Role control
        if user.role == "associate":
            if user not in project.associates.all():
                return HttpResponseForbidden("Not allowed")

        if user.role == "manager":
            if project.manager != user:
                return HttpResponseForbidden("Not allowed")

        if user.role == "client":
            return HttpResponseForbidden("Clients cannot change status")

        project.status = new_status
        project.save()

    return redirect('project_detail', pk=pk)