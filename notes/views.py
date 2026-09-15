from django.shortcuts import get_object_or_404, redirect, render

from .models import Note, Tag


def get_tag(name):
    """Devolve a Tag com esse nome, criando-a se ainda nao existir.

    A busca ignora maiusculas/minusculas para que 'Comida' e 'comida' nao
    virem duas tags diferentes no banco. Nome vazio significa nota sem tag.
    """
    name = (name or '').strip()
    if not name:
        return None

    tag = Tag.objects.filter(name__iexact=name).first()
    if tag is None:
        tag = Tag.objects.create(name=name)
    return tag


def index(request):
    if request.method == 'POST':
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = get_tag(request.POST.get('tag'))
        Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})


def edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.tag = get_tag(request.POST.get('tag'))
        note.save()
        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})


def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('index')
    else:
        return render(request, 'notes/delete.html', {'note': note})


def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': tag.notes.all()})
