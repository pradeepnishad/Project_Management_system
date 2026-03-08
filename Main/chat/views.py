from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Message
from .forms import MessageForm


@login_required
def edit_message(request, pk):
    message = get_object_or_404(Message, pk=pk)

    # Permission check
    if request.user != message.sender and request.user.role != "admin":
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=message.project.pk)
    else:
        form = MessageForm(instance=message)

    return render(request, 'chat/edit_message.html', {'form': form})


@login_required
def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)

    # Permission check
    if request.user != message.sender and request.user.role != "admin":
        return HttpResponseForbidden("Not allowed")

    project_id = message.project.pk
    message.delete()

    return redirect('project_detail', pk=project_id)