import {
  UserActivitiesPerWeek,
  UserActivitiesPerWeekResults,
} from "@/schemas/api/Activities/weekly_activities";
import prisma from "./db-context";
import { MainAbsenceReportRequest } from "@/schemas/api";

function getIsAcceptedStatus(acceptedKey: number) {
  switch (acceptedKey) {
    case 0:
      return "#";
    case 1:
      return "Not Accepted";
    case 2:
      return "Accepted";
    case 3:
      return "Rejected";
    default:
      return "#";
  }
}
function getWeekDayDate(weekStart: Date, dayNo: number) {
  const date = new Date(weekStart);
  date.setDate(date.getDate() + dayNo);
  return date;
}
export async function getTimeSheetDetails(
  searchFilters: MainAbsenceReportRequest = {
    startingDate: undefined,
    endingDate: undefined,
  },
  isLookingForAbsence: boolean = false,
  userId: number = -1
): Promise<UserActivitiesPerWeekResults> {
  const tsActivitiesTimeSheetDetailsOfUser = await prisma.ts_main.findMany({
    select: {
      id: true,
      wd1: true,
      wd2: true,
      wd3: true,
      wd4: true,
      wd5: true,
      wd6: true,
      wd7: true,
      note: true,
      is_accepted: true,
      ts_timesheets: {
        select: {
          id: true,
          created: true,
          last_modified: true,
          status_id: true,
          users: {
            select: {
              id: true,
              name: true,
              middle: true,
              sname: true,
            },
          },
          note: true,
          ts_weeks: {
            select: {
              ts_year: true,
              w_no: true,
              w_start: true,
              w_end: true,
            },
          },
          ts_statuses: {
            select: {
              name: true,
              note: true,
            },
          },
        },
      },
      projects: {
        select: {
          name: true,
          code: true,
          users_projects_ep_idTousers: {
            select: {
              id: true,
              name: true,
              middle: true,
              sname: true,
            },
          },
          users_projects_manager_idTousers: {
            select: {
              id: true,
              name: true,
              middle: true,
              sname: true,
            },
          },
        },
      },
      operations: {
        select: {
          name: true,
        },
      },
      ts_activity_types: {
        select: {
          name: true,
        },
      },
      ts_absence_types: {
        select: {
          name: true,
        },
      },
    },
    where: {
      absence_id: isLookingForAbsence
        ? {
            not: null,
          }
        : null,
      ts_timesheets: {
        ts_weeks: {
          ...(searchFilters.startingDate && {
            w_start: { gt: searchFilters.startingDate },
          }),
          ...(searchFilters.endingDate && {
            w_end: { lt: searchFilters.endingDate },
          }),
        },
        ...(userId != -1 && { user_id: userId }),
      },
    },
    orderBy: {
      ts_timesheets: {
        ts_weeks: {
          w_no: "asc",
        },
      },
    },
  });

  const formattedResults: Array<UserActivitiesPerWeek> =
    tsActivitiesTimeSheetDetailsOfUser.map((act) => ({
      userId: act.ts_timesheets.users.id,
      type: act.ts_activity_types ? act.ts_activity_types.name : "",
      project: act.projects ? act.projects.code : act.note ? act.note : "",
      subProject: act.operations ? act.operations.name : "",
      name: `${act.ts_timesheets.users.name}${
        act.ts_timesheets.users.middle
          ? " " + act.ts_timesheets.users.middle
          : ""
      } ${act.ts_timesheets.users.sname}`,
      week: act.ts_timesheets.ts_weeks.w_no,
      weekStartDate: act.ts_timesheets.ts_weeks.w_start,
      weekEndDate: act.ts_timesheets.ts_weeks.w_end,
      approver: act.projects
        ? act.projects.users_projects_ep_idTousers
          ? act.ts_timesheets.users.id !=
            act.projects.users_projects_ep_idTousers.id
            ? `${act.projects.users_projects_ep_idTousers.name}${
                act.projects.users_projects_ep_idTousers.middle
                  ? " " + act.projects.users_projects_ep_idTousers.middle
                  : ""
              } ${act.projects.users_projects_ep_idTousers.sname}`
            : "Head of Unit"
          : "project_manager"
        : "project_manager",
      approverAction: getIsAcceptedStatus(
        act.is_accepted ? act.is_accepted : 0
      ),
      weekDayOne: act.wd1,
      weekDayOneDate: act.ts_timesheets.ts_weeks.w_start,
      weekDayTwo: act.wd2,
      weekDayTwoDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 1),
      weekDayThree: act.wd3,
      weekDayThreeDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 2),
      weekDayFour: act.wd4,
      weekDayFourDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 3),
      weekDayFive: act.wd5,
      weekDayFiveDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 4),
      weekDaySix: act.wd6,
      weekDaySixDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 5),
      weekDaySeven: act.wd7,
      weekDaySevenDate: getWeekDayDate(act.ts_timesheets.ts_weeks.w_start, 6),
      totalWorkedHoursInWeek: act.wd1
        .plus(act.wd2)
        .plus(act.wd3)
        .plus(act.wd4)
        .plus(act.wd5)
        .plus(act.wd6)
        .plus(act.wd7),
      note: act.projects ? "" : act.note ? act.note : "",
    }));

  const sortedResults: UserActivitiesPerWeekResults = {};
  for (let index = 0; index < formattedResults.length; index++) {
    const act = formattedResults[index];
    if (act.name in sortedResults) {
      sortedResults[act.name].push(act);
    } else {
      sortedResults[act.name] = [act];
    }
  }
  return sortedResults;
}
