using Microsoft.AspNetCore.Mvc;
using RacingRules.Services;
using RacingRules.Views.Racing;

namespace RacingRules.Controllers;

public class RacingController: Controller
{
    private readonly ParticipantsService _participants;
    
    public RacingController(ParticipantsService participants)
    {
        _participants = participants;
    }
    
    public IActionResult Index()
    {
        Views.Racing.Index model = new(_participants.Participants);
        return View(model);
    }

    [HttpPost]
    public IActionResult AddParticipant([FromForm] string firstName, [FromForm] string lastName)
    {
        // Add a new participant
        _participants.Participants.Add(new Participant(firstName, lastName));
        return RedirectToAction("Index");
    }

    [HttpPost]
    public IActionResult StartRace()
    {
        List<LeaderboardEntry> unorderedEntries = [];
        Random random = new();
        foreach (var participant in _participants.Participants)
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
        _participants.Leaderboard = unorderedEntries
            .OrderBy(l => l.TimeForCompletion.TotalSeconds)
            .ToList();

        // Disallow adding participants, probably exist better alternatives than doing this
        _participants.Participants = null!;
        // Simulate racing
        _ = Task.Run(async () =>
        {
            await Task.Delay(TimeSpan.FromSeconds(5));
            // Allow adding participants
            _participants.Participants = [];
        });
        return View();
    }

    public IActionResult Leaderboard()
    {
        return View(new Leaderboard(_participants.Leaderboard));
    }

    [HttpGet("/")]
    public IActionResult Main()
    {
        return Redirect("/Racing");
    }
}