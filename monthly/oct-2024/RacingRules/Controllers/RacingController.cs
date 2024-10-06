using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
using RacingRules.Services;
using RacingRules.Views.Racing;

namespace RacingRules.Controllers;

public class RacingController : Controller
{
    private readonly IMemoryCache _cache;

    public RacingController(IMemoryCache cache)
    {
        _cache = cache;
    }

    public IActionResult Index()
    {
        var participants = GetParticipant();

        Views.Racing.Index model = new(participants.Participants);
        return View(model);
    }

    [HttpPost]
    public IActionResult AddParticipant([FromForm] string firstName, [FromForm] string lastName)
    {
        var participants = GetParticipant();
        participants.Participants.Add(new Participant(firstName, lastName));

        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult StartRace()
    {
        var participants = GetParticipant();

        List<LeaderboardEntry> unorderedEntries = [];
        Random random = new();
        foreach (var participant in participants.Participants)
        {
            unorderedEntries.Add(
                new LeaderboardEntry(
                    participant.FirstName,
                    participant.LastName,
                    timeForCompletion: TimeSpan.FromSeconds(random.Next(10, 100))
                )
            );
        }

        // Ordering from completion time
        participants.Leaderboard = unorderedEntries
            .OrderBy(l => l.TimeForCompletion.TotalSeconds)
            .ToList();

        // Disallow adding participants
        participants.Participants = null!;
        // Simulate racing
        _ = Task.Run(async () =>
        {
            await Task.Delay(TimeSpan.FromSeconds(5));
            // Allow adding participants
            participants.Participants = [];
        });
        return View();
    }

    public IActionResult Leaderboard()
    {
        var participants = GetParticipant();

        return View(new Leaderboard(participants.Leaderboard));
    }

    [HttpGet("/")]
    public IActionResult Main()
    {
        return Redirect("/Racing");
    }

    private ParticipantsService GetParticipant()
    {
        var address = HttpContext.Connection.RemoteIpAddress ?? HttpContext.Connection.LocalIpAddress;
        if (address is null)
        {
            throw new ArgumentException("Couldn't get users IP address");
        }

        ParticipantsService participants;
        if (_cache.TryGetValue(address, out var value))
        {
            participants = (value as ParticipantsService)!;
        }
        else
        {
            participants = new ParticipantsService();
            _cache.Set(address, participants, TimeSpan.FromMinutes(2));
        }

        return participants;
    }
}