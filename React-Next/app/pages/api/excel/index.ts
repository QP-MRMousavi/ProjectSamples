import ExcelJS from "exceljs";

import { NextApiResponse, NextApiRequest } from "next";
import { AuthorizedController, handler } from "@/Core/controller";
import { getTimeSheetDetails } from "@/db/main-export";
import { UserActivitiesPerWeekResults } from "@/schemas/api";

async function get(req: NextApiRequest, res: NextApiResponse) {
  // const data: UserActivitiesPerWeekResults = await getTimeSheetDetails(2024);
  // try {
  //   const workbook = new ExcelJS.Workbook();
  //   //making total worksheet
  //   const sheetAll = workbook.addWorksheet("All");
  //   const workSheetHeadersForTotal = [
  //     "#",
  //     "Name",
  //     "Week",
  //     "Type",
  //     "Project",
  //     "SubProject",
  //     "Approver",
  //     "ApproverAction",
  //     "WD1",
  //     "Note",
  //     "Week day",
  //     "Date",
  //   ];
  //   // Set headers
  //   sheetAll.addRow(workSheetHeadersForTotal);
  //   sheetAll.eachRow({ includeEmpty: false }, function (row, rowNumber) {
  //     row.eachCell((cell, colNumber) => {
  //       cell.fill = {
  //         type: "pattern",
  //         pattern: "solid",
  //         fgColor: { argb: "#fff2cc" }, // Green color code
  //       };
  //     });
  //   });
  //   sheetAll.autoFilter = {
  //     from: {
  //       row: 1, // Row index where headers are located
  //       column: 1, // Column index where filtering should start
  //     },
  //     to: {
  //       row: 1, // Row index where headers are located
  //       column: workSheetHeadersForTotal.length, // Column index where filtering should end
  //     },
  //   };
  //   const userListKeys = Object.keys(data);
  //   let indexNumber = 1;
  //   // Add data rows
  //   for (let index = 1; index <= 7; index++) {
  //     userListKeys.map((key) => {
  //       // Add data rows
  //       data[key].map((record) => {
  //         let currentWorkingHourInWeekDay = "0";
  //         let currentWorkingDayDate = new Date();
  //         switch (index) {
  //           case 1:
  //             currentWorkingHourInWeekDay = record.weekDayOne.toString();
  //             currentWorkingDayDate = record.weekDayOneDate;
  //             break;
  //           case 2:
  //             currentWorkingHourInWeekDay = record.weekDayTwo.toString();
  //             currentWorkingDayDate = record.weekDayTwoDate;
  //             break;
  //           case 3:
  //             currentWorkingHourInWeekDay = record.weekDayThree.toString();
  //             currentWorkingDayDate = record.weekDayThreeDate;
  //             break;
  //           case 4:
  //             currentWorkingHourInWeekDay = record.weekDayFour.toString();
  //             currentWorkingDayDate = record.weekDayFourDate;
  //             break;
  //           case 5:
  //             currentWorkingHourInWeekDay = record.weekDayFive.toString();
  //             currentWorkingDayDate = record.weekDayFiveDate;
  //             break;
  //           case 6:
  //             currentWorkingHourInWeekDay = record.weekDaySix.toString();
  //             currentWorkingDayDate = record.weekDaySixDate;
  //             break;
  //           case 7:
  //             currentWorkingHourInWeekDay = record.weekDaySix.toString();
  //             currentWorkingDayDate = record.weekDaySixDate;
  //             break;
  //           default:
  //             break;
  //         }
  //         const rowData: Array<any> = [
  //           indexNumber,
  //           record.name,
  //           record.week,
  //           record.type,
  //           record.project,
  //           record.subProject,
  //           record.approver,
  //           record.approverAction,
  //           currentWorkingHourInWeekDay,
  //           record.note,
  //           index,
  //           currentWorkingDayDate,
  //         ];
  //         indexNumber += 1;
  //         sheetAll.addRow(rowData);
  //       });
  //     });
  //   }
  //   // Iterate through each key in data and create a sheet for each
  //   Object.keys(data).map((key) => {
  //     if (Object.hasOwnProperty.call(data, key)) {
  //       const sheet = workbook.addWorksheet(key);
  //       // Set headers
  //       const headers = Object.keys(data[key][0]);
  //       sheet.addRow(headers);
  //       // Add data rows
  //       data[key].map((record) => {
  //         const rowData = headers.map((header) => (record as any)[header]);
  //         sheet.addRow(rowData);
  //       });
  //     }
  //   });
  //   // Write workbook to file
  //   const buffer = await workbook.xlsx.writeBuffer();
  //   // Set response headers
  //   res.setHeader(
  //     "Content-Type",
  //     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  //   );
  //   res.setHeader("Content-Disposition", 'attachment; filename="example.xlsx"');
  //   // Send the buffer as the response
  //   res.send(Buffer.from(buffer));
  // } catch (error) {
  //   console.error("Error generating Excel file:", error);
  //   res.status(500).end();
  // }
}

export default handler(
  new AuthorizedController({
    get: get,
    put: null,
    post: null,
    delete: null,
  })
);
