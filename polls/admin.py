from django.contrib import admin
from .models import Election, Candidate, Vote

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 1

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active', 'total_votes')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    inlines = [CandidateInline]
    
    def total_votes(self, obj):
        return obj.votes.count()

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'vote_count')
    list_filter = ('election',)
    search_fields = ('name', 'bio')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'election', 'candidate', 'timestamp', 'verification_code')
    list_filter = ('election', 'timestamp')
    search_fields = ('user__username', 'verification_code')
    readonly_fields = ('user', 'election', 'candidate', 'timestamp', 'verification_code')